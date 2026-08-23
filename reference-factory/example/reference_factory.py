"""Minimal executable companion for the accountable-factory contracts.

Teaching code only: SQLite supplies durable records and transactions, while a
caller supplies model, policy, verifier, and delivery adapters.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ALLOWED = {
    "ADMITTED": {"RUNNING", "CANCELLED"},
    "RUNNING": {"CANDIDATE", "FAILED", "PARTIAL", "CANCELLED"},
    "CANDIDATE": {"VERIFYING", "READY"},
    "VERIFYING": {"DECISION_REQUIRED", "READY"},
    "DECISION_REQUIRED": {"APPROVED", "REJECTED", "READY"},
    "APPROVED": {"RELEASED"},
    "RELEASED": {"OBSERVING"},
}


class ContractViolation(RuntimeError):
    pass


@dataclass(frozen=True)
class WorkOrder:
    id: str
    version: int
    state: str
    intent: dict


class Factory:
    def __init__(self, database: str | Path):
        self.db = sqlite3.connect(str(database))
        self.db.row_factory = sqlite3.Row
        self.db.executescript(
            """
            PRAGMA journal_mode=WAL;
            CREATE TABLE IF NOT EXISTS work_orders(
              id TEXT PRIMARY KEY, version INTEGER NOT NULL, state TEXT NOT NULL,
              intent_json TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS events(
              seq INTEGER PRIMARY KEY AUTOINCREMENT, work_order_id TEXT NOT NULL,
              kind TEXT NOT NULL, body_json TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS candidates(
              digest TEXT PRIMARY KEY, work_order_id TEXT NOT NULL,
              work_order_version INTEGER NOT NULL, content BLOB NOT NULL
            );
            CREATE TABLE IF NOT EXISTS verdicts(
              candidate_digest TEXT NOT NULL, criterion TEXT NOT NULL,
              source TEXT NOT NULL, result TEXT NOT NULL,
              PRIMARY KEY(candidate_digest, criterion, source)
            );
            CREATE TABLE IF NOT EXISTS operations(
              operation_id TEXT PRIMARY KEY, work_order_id TEXT NOT NULL,
              status TEXT NOT NULL, effect_ref TEXT
            );
            """
        )

    def admit(self, intent: dict) -> WorkOrder:
        required = {"promise", "criteria", "prohibitions", "owner"}
        missing = sorted(required - intent.keys())
        if missing:
            raise ContractViolation(f"intent missing: {', '.join(missing)}")
        work_order_id = str(uuid.uuid4())
        body = json.dumps(intent, sort_keys=True)
        with self.db:
            self.db.execute(
                "INSERT INTO work_orders VALUES (?, 1, 'ADMITTED', ?)",
                (work_order_id, body),
            )
            self._event(work_order_id, "admitted", {"version": 1})
        return self.load(work_order_id)

    def load(self, work_order_id: str) -> WorkOrder:
        row = self.db.execute(
            "SELECT * FROM work_orders WHERE id = ?", (work_order_id,)
        ).fetchone()
        if row is None:
            raise KeyError(work_order_id)
        return WorkOrder(row["id"], row["version"], row["state"], json.loads(row["intent_json"]))

    def transition(self, work_order_id: str, expected_version: int, target: str, actor: str) -> WorkOrder:
        current = self.load(work_order_id)
        if current.version != expected_version:
            raise ContractViolation("stale work-order version")
        if target not in ALLOWED.get(current.state, set()):
            raise ContractViolation(f"illegal transition: {current.state} -> {target}")
        with self.db:
            changed = self.db.execute(
                "UPDATE work_orders SET state=?, version=version+1 WHERE id=? AND version=?",
                (target, work_order_id, expected_version),
            ).rowcount
            if changed != 1:
                raise ContractViolation("concurrent transition")
            self._event(work_order_id, "transition", {"from": current.state, "to": target, "actor": actor})
        return self.load(work_order_id)

    def record_candidate(self, work_order_id: str, expected_version: int, content: bytes) -> str:
        current = self.load(work_order_id)
        if current.version != expected_version or current.state != "RUNNING":
            raise ContractViolation("candidate does not belong to current running version")
        digest = hashlib.sha256(content).hexdigest()
        with self.db:
            self.db.execute(
                "INSERT OR IGNORE INTO candidates VALUES (?, ?, ?, ?)",
                (digest, work_order_id, expected_version, content),
            )
            self._event(work_order_id, "candidate", {"digest": digest})
        return digest

    def verdict(self, digest: str, criterion: str, source: str, result: str, *, producer: bool = False) -> None:
        if producer:
            raise ContractViolation("producer claim cannot be a decisive verdict")
        if result not in {"pass", "fail", "unresolved", "error"}:
            raise ContractViolation("unknown verdict")
        if self.db.execute("SELECT 1 FROM candidates WHERE digest=?", (digest,)).fetchone() is None:
            raise ContractViolation("evidence references an unknown candidate")
        with self.db:
            self.db.execute(
                "INSERT OR REPLACE INTO verdicts VALUES (?, ?, ?, ?)",
                (digest, criterion, source, result),
            )

    def evidence_satisfies(self, digest: str, required: Iterable[str]) -> bool:
        return all(self.evidence_status(digest, criterion) == "pass" for criterion in required)

    def evidence_status(self, digest: str, criterion: str) -> str:
        """Summarize evidence without allowing one pass to erase disagreement."""
        results = {
            row[0]
            for row in self.db.execute(
                "SELECT result FROM verdicts WHERE candidate_digest=? AND criterion=?",
                (digest, criterion),
            )
        }
        if not results:
            return "missing"
        if results == {"pass"}:
            return "pass"
        if len(results) > 1:
            return "conflict"
        return next(iter(results))

    def record_event(self, work_order_id: str, kind: str, body: dict) -> None:
        """Record a material teaching event in the durable decision chain."""
        with self.db:
            self._event(work_order_id, kind, body)

    def events(self, work_order_id: str) -> list[dict]:
        rows = self.db.execute(
            "SELECT seq, kind, body_json FROM events WHERE work_order_id=? ORDER BY seq",
            (work_order_id,),
        )
        return [
            {"seq": row["seq"], "kind": row["kind"], "body": json.loads(row["body_json"])}
            for row in rows
        ]

    def begin_operation(self, work_order_id: str, operation_id: str) -> str:
        """Persist intent-to-act. Reusing an ID never creates a second operation."""
        with self.db:
            self.db.execute(
                "INSERT OR IGNORE INTO operations VALUES (?, ?, 'INTENDED', NULL)",
                (operation_id, work_order_id),
            )
        return self.operation_status(operation_id)

    def complete_operation(self, operation_id: str, effect_ref: str) -> None:
        with self.db:
            changed = self.db.execute(
                "UPDATE operations SET status='COMPLETED', effect_ref=? "
                "WHERE operation_id=? AND status IN ('INTENDED','INDETERMINATE')",
                (effect_ref, operation_id),
            ).rowcount
            if changed != 1:
                row = self.db.execute(
                    "SELECT effect_ref FROM operations WHERE operation_id=? AND status='COMPLETED'",
                    (operation_id,),
                ).fetchone()
                if row is None or row[0] != effect_ref:
                    raise ContractViolation("operation completion conflicts with durable receipt")

    def mark_indeterminate(self, operation_id: str) -> None:
        with self.db:
            self.db.execute(
                "UPDATE operations SET status='INDETERMINATE' WHERE operation_id=? AND status='INTENDED'",
                (operation_id,),
            )

    def reconcile(self, operation_id: str, observed_effect_ref: str | None) -> str:
        status = self.operation_status(operation_id)
        if status == "COMPLETED":
            return status
        if observed_effect_ref is None:
            return "INDETERMINATE"
        self.complete_operation(operation_id, observed_effect_ref)
        return "COMPLETED"

    def operation_status(self, operation_id: str) -> str:
        row = self.db.execute(
            "SELECT status FROM operations WHERE operation_id=?", (operation_id,)
        ).fetchone()
        if row is None:
            raise KeyError(operation_id)
        return row[0]

    def _event(self, work_order_id: str, kind: str, body: dict) -> None:
        self.db.execute(
            "INSERT INTO events(work_order_id,kind,body_json) VALUES (?,?,?)",
            (work_order_id, kind, json.dumps(body, sort_keys=True)),
        )
