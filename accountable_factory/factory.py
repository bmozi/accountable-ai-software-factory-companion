"""Durable, policy-bound teaching core for an accountable software factory.

© 2026 John Briggs — MIT licensed; see ../LICENSE-CODE.
"""

from __future__ import annotations

import json
import sqlite3
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from .contracts import ArtifactError, require_valid, sha256_digest
from .policy import PolicyEngine, PolicyViolation


ALLOWED = {
    "ADMITTED": {"RUNNING", "CANCELLED"},
    "RUNNING": {"CANDIDATE", "FAILED", "PARTIAL", "CANCELLED"},
    "CANDIDATE": {"VERIFYING", "CANCELLED"},
    "VERIFYING": {"DECISION_REQUIRED", "FAILED", "CANCELLED"},
    "DECISION_REQUIRED": {"APPROVED", "REJECTED", "RUNNING", "CANCELLED"},
    "APPROVED": {"RELEASING", "CANCELLED"},
    "RELEASING": {"RELEASED", "PARTIAL", "FAILED"},
    "RELEASED": {"OBSERVING", "ROLLED_BACK"},
    "OBSERVING": {
        "EFFECTIVE", "INEFFECTIVE", "INSUFFICIENT", "HARMFUL", "ROLLED_BACK"
    },
    "EFFECTIVE": {"RETIRED"},
    "INEFFECTIVE": {"RETIRED"},
    "INSUFFICIENT": {"OBSERVING", "RETIRED"},
    "HARMFUL": {"ROLLED_BACK", "RETIRED"},
}


class ContractViolation(RuntimeError):
    pass


@dataclass(frozen=True)
class WorkOrder:
    id: str
    version: int
    state: str
    document: dict[str, Any]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


class Factory:
    """A small reference implementation of the book's accountability spine."""

    def __init__(self, database: str | Path, policy: PolicyEngine):
        self.db = sqlite3.connect(str(database))
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA foreign_keys=ON")
        self.policy = policy
        self._initialize()

    def _initialize(self) -> None:
        old = self.db.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='work_orders'"
        ).fetchone()
        if old is not None:
            columns = {
                row[1] for row in self.db.execute("PRAGMA table_info(work_orders)")
            }
            if "intent_json" in columns:
                raise ContractViolation(
                    "v1.0 teaching database uses the retired split contract; "
                    "start a v1.1 database after exporting any learning records"
                )
            if "candidate_digest" not in columns:
                self.db.execute("ALTER TABLE work_orders ADD COLUMN candidate_digest TEXT")
        self.db.executescript(
            """
            PRAGMA journal_mode=WAL;
            CREATE TABLE IF NOT EXISTS work_orders(
              id TEXT PRIMARY KEY,
              version INTEGER NOT NULL,
              state TEXT NOT NULL,
              document_json TEXT NOT NULL,
              candidate_digest TEXT
            );
            CREATE TABLE IF NOT EXISTS events(
              seq INTEGER PRIMARY KEY AUTOINCREMENT,
              work_order_id TEXT NOT NULL REFERENCES work_orders(id),
              kind TEXT NOT NULL,
              actor_id TEXT NOT NULL,
              body_json TEXT NOT NULL,
              created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS candidates(
              work_order_id TEXT NOT NULL REFERENCES work_orders(id),
              digest TEXT NOT NULL,
              work_order_version INTEGER NOT NULL,
              producer_id TEXT NOT NULL,
              content BLOB NOT NULL,
              created_at TEXT NOT NULL,
              PRIMARY KEY(work_order_id, digest)
            );
            CREATE TABLE IF NOT EXISTS evidence_records(
              id TEXT PRIMARY KEY,
              work_order_id TEXT NOT NULL REFERENCES work_orders(id),
              candidate_digest TEXT NOT NULL,
              criterion_id TEXT NOT NULL,
              document_json TEXT NOT NULL,
              created_at TEXT NOT NULL,
              FOREIGN KEY(work_order_id, candidate_digest)
                REFERENCES candidates(work_order_id, digest)
            );
            CREATE TABLE IF NOT EXISTS dispositions(
              id TEXT PRIMARY KEY,
              work_order_id TEXT NOT NULL REFERENCES work_orders(id),
              candidate_digest TEXT NOT NULL,
              actor_id TEXT NOT NULL,
              decision TEXT NOT NULL,
              reason TEXT NOT NULL,
              expires_at TEXT,
              created_at TEXT NOT NULL,
              FOREIGN KEY(work_order_id, candidate_digest)
                REFERENCES candidates(work_order_id, digest)
            );
            CREATE TABLE IF NOT EXISTS operations(
              operation_id TEXT PRIMARY KEY,
              work_order_id TEXT NOT NULL REFERENCES work_orders(id),
              status TEXT NOT NULL,
              effect_ref TEXT,
              reconciliation_evidence TEXT,
              updated_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS receipts(
              id TEXT PRIMARY KEY,
              work_order_id TEXT NOT NULL REFERENCES work_orders(id),
              operation_id TEXT NOT NULL UNIQUE REFERENCES operations(operation_id),
              document_json TEXT NOT NULL,
              created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS outcomes(
              id TEXT PRIMARY KEY,
              receipt_id TEXT NOT NULL REFERENCES receipts(id),
              document_json TEXT NOT NULL,
              created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS attempts(
              id TEXT PRIMARY KEY,
              work_order_id TEXT NOT NULL REFERENCES work_orders(id),
              parent_id TEXT REFERENCES attempts(id),
              kind TEXT NOT NULL,
              state TEXT NOT NULL,
              reserved_units REAL NOT NULL,
              result_json TEXT,
              created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS revoked_capabilities(
              work_order_id TEXT NOT NULL REFERENCES work_orders(id),
              dimension TEXT NOT NULL,
              value TEXT NOT NULL,
              actor_id TEXT NOT NULL,
              created_at TEXT NOT NULL,
              PRIMARY KEY(work_order_id, dimension, value)
            );
            CREATE TABLE IF NOT EXISTS leases(
              work_order_id TEXT PRIMARY KEY REFERENCES work_orders(id),
              holder TEXT NOT NULL,
              expires_at TEXT NOT NULL,
              epoch INTEGER NOT NULL,
              updated_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS learnings(
              id TEXT PRIMARY KEY,
              work_order_id TEXT NOT NULL REFERENCES work_orders(id),
              state TEXT NOT NULL,
              claim TEXT NOT NULL,
              scope_json TEXT NOT NULL,
              evidence_json TEXT NOT NULL,
              expires_at TEXT,
              updated_at TEXT NOT NULL
            );
            PRAGMA user_version=2;
            """
        )

    def close(self) -> None:
        self.db.close()

    def admit(self, document: dict[str, Any], actor: str) -> WorkOrder:
        try:
            require_valid(document)
        except ArtifactError as exc:
            raise ContractViolation(str(exc)) from exc
        if document["kind"] != "WorkOrder":
            raise ContractViolation("admission requires a WorkOrder artifact")
        if actor != document["owner"]:
            raise ContractViolation("only the named Work Order owner may admit it")
        policy_errors = self.policy.evaluate_work_order(document)
        if policy_errors:
            raise ContractViolation("; ".join(policy_errors))
        body = json.dumps(document, sort_keys=True)
        with self.db:
            self.db.execute(
                "INSERT INTO work_orders(id,version,state,document_json,candidate_digest) VALUES (?, ?, 'ADMITTED', ?, NULL)",
                (document["id"], document["version"], body),
            )
            self._event(document["id"], "admitted", actor, {"version": document["version"]})
        return self.load(document["id"])

    def load(self, work_order_id: str) -> WorkOrder:
        row = self.db.execute(
            "SELECT * FROM work_orders WHERE id=?", (work_order_id,)
        ).fetchone()
        if row is None:
            raise KeyError(work_order_id)
        return WorkOrder(
            row["id"], row["version"], row["state"], json.loads(row["document_json"])
        )

    def update_intent(
        self, work_order_id: str, expected_version: int, document: dict[str, Any], actor: str
    ) -> WorkOrder:
        current = self.load(work_order_id)
        if actor != current.document["owner"]:
            raise ContractViolation("only the owner may update intent")
        if current.version != expected_version:
            raise ContractViolation("stale work-order version")
        if current.state != "ADMITTED":
            raise ContractViolation("intent may change only before execution")
        if document.get("id") != work_order_id or document.get("version") != expected_version + 1:
            raise ContractViolation("updated intent must preserve id and increment version once")
        try:
            require_valid(document)
        except ArtifactError as exc:
            raise ContractViolation(str(exc)) from exc
        policy_errors = self.policy.evaluate_work_order(document)
        if policy_errors:
            raise ContractViolation("; ".join(policy_errors))
        with self.db:
            changed = self.db.execute(
                "UPDATE work_orders SET version=?, document_json=? WHERE id=? AND version=?",
                (document["version"], json.dumps(document, sort_keys=True), work_order_id, expected_version),
            ).rowcount
            if changed != 1:
                raise ContractViolation("concurrent intent update")
            self._event(work_order_id, "intent_updated", actor, {"from": expected_version, "to": document["version"]})
        return self.load(work_order_id)

    def start(self, work_order_id: str, expected_version: int, actor: str) -> WorkOrder:
        current = self.load(work_order_id)
        if actor != current.document["owner"]:
            raise ContractViolation("only the owner may start execution")
        return self._transition(work_order_id, expected_version, "RUNNING", actor)

    def transition(
        self, work_order_id: str, expected_version: int, target: str, actor: str
    ) -> WorkOrder:
        """Guarded public transition used by drills; cannot bypass evidence or roles."""
        current = self.load(work_order_id)
        if target in {"APPROVED", "REJECTED", "RUNNING"} and current.state == "DECISION_REQUIRED":
            raise ContractViolation("use decide() so disposition is durable")
        if target in {"RELEASING", "RELEASED", "OBSERVING"}:
            raise ContractViolation("use release and observation methods")
        if target == "ROLLED_BACK" and actor not in {
            current.document["consequenceOwner"], current.document["recovery"]["owner"]
        }:
            raise ContractViolation("rollback requires consequence or recovery owner")
        if target == "RETIRED" and actor != current.document["consequenceOwner"]:
            raise ContractViolation("retirement requires consequence owner")
        return self._transition(work_order_id, expected_version, target, actor)

    def acquire_lease(
        self, work_order_id: str, actor: str, now: str, expires_at: str
    ) -> int:
        """Acquire or recover a durable lease; an unexpired lease cannot be stolen."""
        work = self.load(work_order_id)
        admitted = {
            work.document["owner"], work.document["producerId"],
            work.document["releaseOwner"], work.document["recovery"]["owner"],
        }
        if actor not in admitted or expires_at <= now:
            raise ContractViolation("lease holder or expiry is not admitted")
        row = self.db.execute(
            "SELECT * FROM leases WHERE work_order_id=?", (work_order_id,)
        ).fetchone()
        if row is not None and row["expires_at"] > now and row["holder"] != actor:
            raise ContractViolation("active lease belongs to another holder")
        epoch = 1 if row is None else row["epoch"] + 1
        with self.db:
            self.db.execute(
                "INSERT INTO leases VALUES (?,?,?,?,?) ON CONFLICT(work_order_id) "
                "DO UPDATE SET holder=excluded.holder, expires_at=excluded.expires_at, "
                "epoch=excluded.epoch, updated_at=excluded.updated_at",
                (work_order_id, actor, expires_at, epoch, _now()),
            )
            self._event(work_order_id, "lease_acquired", actor, {"epoch": epoch, "expiresAt": expires_at})
        return epoch

    def _transition(
        self, work_order_id: str, expected_version: int, target: str, actor: str
    ) -> WorkOrder:
        current = self.load(work_order_id)
        if current.version != expected_version:
            raise ContractViolation("stale work-order version")
        if target not in ALLOWED.get(current.state, set()):
            raise ContractViolation(f"illegal transition: {current.state} -> {target}")
        with self.db:
            self._transition_locked(current, target, actor)
        return self.load(work_order_id)

    def _transition_locked(self, current: WorkOrder, target: str, actor: str) -> None:
        if target == "RUNNING":
            changed = self.db.execute(
                "UPDATE work_orders SET state=?, version=version+1, candidate_digest=NULL WHERE id=? AND version=?",
                (target, current.id, current.version),
            ).rowcount
        else:
            changed = self.db.execute(
                "UPDATE work_orders SET state=?, version=version+1 WHERE id=? AND version=?",
                (target, current.id, current.version),
            ).rowcount
        if changed != 1:
            raise ContractViolation("concurrent transition")
        self._event(
            current.id, "transition", actor,
            {"from": current.state, "to": target, "version": current.version + 1},
        )

    def assert_capability(
        self, work_order_id: str, dimension: str, value: str, actor: str
    ) -> None:
        work = self.load(work_order_id)
        revoked = self.db.execute(
            "SELECT 1 FROM revoked_capabilities WHERE work_order_id=? AND dimension=? AND value=?",
            (work_order_id, dimension, value),
        ).fetchone()
        try:
            if revoked is not None:
                raise PolicyViolation(f"authority revoked: {dimension}={value}")
            self.policy.assert_authority(work.document, dimension, value)
        except PolicyViolation as exc:
            with self.db:
                self._event(work_order_id, "authority_denied", actor, {"dimension": dimension, "value": value, "reason": str(exc)})
            raise ContractViolation(str(exc)) from exc
        with self.db:
            self._event(work_order_id, "authority_used", actor, {"dimension": dimension, "value": value})

    def revoke_capability(
        self, work_order_id: str, dimension: str, value: str, actor: str
    ) -> None:
        work = self.load(work_order_id)
        if actor not in {work.document["owner"], work.document["consequenceOwner"]}:
            raise ContractViolation("revocation requires owner or consequence owner")
        with self.db:
            self.db.execute(
                "INSERT OR IGNORE INTO revoked_capabilities VALUES (?,?,?,?,?)",
                (work_order_id, dimension, value, actor, _now()),
            )
            self._event(work_order_id, "authority_revoked", actor, {"dimension": dimension, "value": value})

    def record_candidate(
        self, work_order_id: str, expected_version: int, content: bytes, actor: str
    ) -> str:
        work = self.load(work_order_id)
        if work.version != expected_version or work.state != "RUNNING":
            raise ContractViolation("candidate does not belong to current running version")
        if actor != work.document["producerId"]:
            raise ContractViolation("candidate actor is not the admitted producer")
        digest = sha256_digest(content)
        try:
            with self.db:
                self.db.execute(
                    "INSERT INTO candidates VALUES (?,?,?,?,?,?)",
                    (work_order_id, digest, expected_version, actor, content, _now()),
                )
                self.db.execute(
                    "UPDATE work_orders SET candidate_digest=? WHERE id=? AND version=?",
                    (digest, work_order_id, expected_version),
                )
                self._event(work_order_id, "candidate_recorded", actor, {"digest": digest})
                self._transition_locked(work, "CANDIDATE", actor)
        except sqlite3.IntegrityError as exc:
            raise ContractViolation("candidate already exists for this Work Order") from exc
        return digest

    def begin_verification(self, work_order_id: str, actor: str) -> WorkOrder:
        work = self.load(work_order_id)
        return self._transition(work_order_id, work.version, "VERIFYING", actor)

    def record_evidence(self, document: dict[str, Any], actor: str) -> None:
        try:
            require_valid(document)
        except ArtifactError as exc:
            raise ContractViolation(str(exc)) from exc
        if document["kind"] != "EvidenceRecord":
            raise ContractViolation("record_evidence requires an EvidenceRecord")
        work = self.load(document["workOrderId"])
        if work.state not in {"CANDIDATE", "VERIFYING", "DECISION_REQUIRED"}:
            raise ContractViolation("evidence is not admissible in the current state")
        if document["producerId"] != work.document["producerId"]:
            raise ContractViolation("evidence producer does not match the Work Order")
        if actor != document["evaluator"]["actorId"]:
            raise ContractViolation("evidence actor does not match evaluator identity")
        criterion_ids = {item["id"] for item in work.document["criteria"]}
        if document["criterionId"] not in criterion_ids:
            raise ContractViolation("evidence names an undeclared criterion")
        candidate = self.db.execute(
            "SELECT 1 FROM candidates WHERE work_order_id=? AND digest=?",
            (work.id, document["candidateDigest"]),
        ).fetchone()
        if candidate is None:
            raise ContractViolation("evidence references a candidate owned by another or unknown Work Order")
        with self.db:
            self.db.execute(
                "INSERT INTO evidence_records VALUES (?,?,?,?,?,?)",
                (
                    document["id"], work.id, document["candidateDigest"],
                    document["criterionId"], json.dumps(document, sort_keys=True), _now(),
                ),
            )
            self._event(work.id, "evidence_recorded", actor, {"id": document["id"], "criterion": document["criterionId"], "result": document["result"]})

    def evidence_status(self, work_order_id: str, digest: str, criterion: str) -> str:
        rows = self.db.execute(
            "SELECT document_json FROM evidence_records WHERE work_order_id=? AND candidate_digest=? AND criterion_id=?",
            (work_order_id, digest, criterion),
        )
        documents = [json.loads(row[0]) for row in rows]
        results = {
            document["result"] for document in documents
            if document.get("decisive")
            and document.get("evaluator", {}).get("actorId") != document.get("producerId")
        }
        if not results:
            return "missing"
        if results == {"pass"}:
            return "pass"
        if len(results) > 1:
            return "conflict"
        return next(iter(results))

    def evidence_satisfies(
        self, work_order_id: str, digest: str, required: Iterable[str]
    ) -> bool:
        return all(
            self.evidence_status(work_order_id, digest, criterion) == "pass"
            for criterion in required
        )

    def request_decision(self, work_order_id: str, digest: str, actor: str) -> WorkOrder:
        work = self.load(work_order_id)
        if work.state != "VERIFYING":
            raise ContractViolation("decision may be requested only after verification begins")
        required = work.document["evidenceFloor"]
        current_digest = self.db.execute(
            "SELECT candidate_digest FROM work_orders WHERE id=?", (work.id,)
        ).fetchone()[0]
        if digest != current_digest:
            raise ContractViolation("decision evidence does not belong to the current candidate")
        if any(self.evidence_status(work.id, digest, criterion) == "missing" for criterion in required):
            raise ContractViolation("declared evidence floor is incomplete")
        return self._transition(work.id, work.version, "DECISION_REQUIRED", actor)

    def decide(
        self,
        work_order_id: str,
        digest: str,
        actor: str,
        decision: str,
        reason: str,
        expires_at: str | None = None,
    ) -> WorkOrder:
        work = self.load(work_order_id)
        if work.state != "DECISION_REQUIRED":
            raise ContractViolation("disposition requires DECISION_REQUIRED state")
        current_digest = self.db.execute(
            "SELECT candidate_digest FROM work_orders WHERE id=?", (work.id,)
        ).fetchone()[0]
        if digest != current_digest:
            raise ContractViolation("disposition does not name the current candidate")
        if actor != work.document["consequenceOwner"] or actor == work.document["producerId"]:
            raise ContractViolation("disposition requires the independent consequence owner")
        if decision not in {"approve", "reject", "repair", "exception"}:
            raise ContractViolation("unknown disposition")
        if decision == "approve" and not self.evidence_satisfies(
            work.id, digest, work.document["evidenceFloor"]
        ):
            raise ContractViolation("approval requires every declared evidence criterion to pass")
        if decision == "exception" and not expires_at:
            raise ContractViolation("exception requires expiry")
        target = {
            "approve": "APPROVED", "exception": "APPROVED",
            "reject": "REJECTED", "repair": "RUNNING",
        }[decision]
        disposition_id = f"DSP-{uuid.uuid4()}"
        with self.db:
            self.db.execute(
                "INSERT INTO dispositions VALUES (?,?,?,?,?,?,?,?)",
                (disposition_id, work.id, digest, actor, decision, reason, expires_at, _now()),
            )
            self._event(work.id, "disposition_recorded", actor, {"id": disposition_id, "decision": decision, "expiresAt": expires_at})
            self._transition_locked(work, target, actor)
        return self.load(work.id)

    def create_attempt(
        self,
        work_order_id: str,
        attempt_id: str,
        actor: str,
        reserved_units: float,
        kind: str = "main",
        parent_id: str | None = None,
    ) -> None:
        work = self.load(work_order_id)
        if kind not in {"main", "repair", "child"} or reserved_units < 0:
            raise ContractViolation("invalid attempt reservation")
        if actor not in {work.document["owner"], work.document["producerId"]}:
            raise ContractViolation("attempt actor is not admitted")
        if kind == "child":
            parent = self.db.execute(
                "SELECT * FROM attempts WHERE id=?", (parent_id,)
            ).fetchone()
            if parent is None or parent["work_order_id"] != work.id or parent["state"] != "ACTIVE":
                raise ContractViolation("child requires an active parent in the same Work Order")
            used = self.db.execute(
                "SELECT COALESCE(sum(reserved_units),0) FROM attempts WHERE parent_id=?",
                (parent_id,),
            ).fetchone()[0]
            if used + reserved_units > parent["reserved_units"]:
                raise ContractViolation("child budgets exceed parent reservation")
        else:
            limit_key = "attempts" if kind == "main" else "repairAttempts"
            count = self.db.execute(
                "SELECT count(*) FROM attempts WHERE work_order_id=? AND kind=?",
                (work.id, kind),
            ).fetchone()[0]
            if count >= work.document["budgets"][limit_key]:
                raise ContractViolation(f"{kind} attempt budget exhausted")
            used = self.db.execute(
                "SELECT COALESCE(sum(reserved_units),0) FROM attempts WHERE work_order_id=? AND kind IN ('main','repair')",
                (work.id,),
            ).fetchone()[0]
            if used + reserved_units > work.document["budgets"]["costUnits"]:
                raise ContractViolation("cost budget exhausted")
        with self.db:
            self.db.execute(
                "INSERT INTO attempts VALUES (?,?,?,?,?,?,?,?)",
                (attempt_id, work.id, parent_id, kind, "ACTIVE", reserved_units, None, _now()),
            )
            self._event(work.id, "attempt_reserved", actor, {"id": attempt_id, "kind": kind, "units": reserved_units, "parent": parent_id})

    def cancel_attempt(self, attempt_id: str, actor: str) -> None:
        row = self.db.execute("SELECT * FROM attempts WHERE id=?", (attempt_id,)).fetchone()
        if row is None:
            raise KeyError(attempt_id)
        with self.db:
            self.db.execute(
                "WITH RECURSIVE descendants(id) AS (SELECT id FROM attempts WHERE id=? UNION ALL SELECT a.id FROM attempts a JOIN descendants d ON a.parent_id=d.id) UPDATE attempts SET state='CANCELLED' WHERE id IN (SELECT id FROM descendants)",
                (attempt_id,),
            )
            self._event(row["work_order_id"], "attempt_cancelled", actor, {"id": attempt_id, "cascade": True})

    def complete_attempt(self, attempt_id: str, actor: str, result: dict[str, Any]) -> None:
        row = self.db.execute("SELECT * FROM attempts WHERE id=?", (attempt_id,)).fetchone()
        if row is None:
            raise KeyError(attempt_id)
        if row["state"] != "ACTIVE":
            raise ContractViolation("late attempt result cannot mutate terminal attempt")
        if row["parent_id"]:
            parent = self.db.execute("SELECT state FROM attempts WHERE id=?", (row["parent_id"],)).fetchone()
            if parent is None or parent[0] != "ACTIVE":
                raise ContractViolation("late child result cannot mutate terminal parent")
        with self.db:
            self.db.execute(
                "UPDATE attempts SET state='COMPLETED', result_json=? WHERE id=?",
                (json.dumps(result, sort_keys=True), attempt_id),
            )
            self._event(row["work_order_id"], "attempt_completed", actor, {"id": attempt_id})

    def begin_release(self, work_order_id: str, operation_id: str, actor: str) -> WorkOrder:
        work = self.load(work_order_id)
        if work.state != "APPROVED" or actor != work.document["releaseOwner"]:
            raise ContractViolation("release requires APPROVED state and named release owner")
        existing = self.db.execute(
            "SELECT work_order_id FROM operations WHERE operation_id=?", (operation_id,)
        ).fetchone()
        if existing is not None:
            if existing[0] != work.id:
                raise ContractViolation("operation identity already belongs to another Work Order")
            raise ContractViolation("operation identity already exists")
        with self.db:
            self.db.execute(
                "INSERT INTO operations VALUES (?,?, 'INTENDED', NULL, NULL, ?)",
                (operation_id, work.id, _now()),
            )
            self._event(work.id, "operation_intended", actor, {"operationId": operation_id})
            self._transition_locked(work, "RELEASING", actor)
        return self.load(work.id)

    def mark_indeterminate(self, operation_id: str, actor: str) -> None:
        row = self._operation(operation_id)
        work = self.load(row["work_order_id"])
        if actor not in {work.document["releaseOwner"], work.document["recovery"]["owner"]}:
            raise ContractViolation("operation recovery requires release or recovery owner")
        with self.db:
            changed = self.db.execute(
                "UPDATE operations SET status='INDETERMINATE', updated_at=? WHERE operation_id=? AND status='INTENDED'",
                (_now(), operation_id),
            ).rowcount
            if changed != 1:
                raise ContractViolation("only an intended operation may become indeterminate")
            self._event(row["work_order_id"], "operation_indeterminate", actor, {"operationId": operation_id})

    def complete_operation(self, operation_id: str, effect_ref: str, actor: str) -> None:
        row = self._operation(operation_id)
        work = self.load(row["work_order_id"])
        if actor != work.document["releaseOwner"]:
            raise ContractViolation("operation completion requires release owner")
        with self.db:
            changed = self.db.execute(
                "UPDATE operations SET status='COMPLETED', effect_ref=?, updated_at=? WHERE operation_id=? AND status='INTENDED'",
                (effect_ref, _now(), operation_id),
            ).rowcount
            if changed != 1:
                if row["status"] == "COMPLETED" and row["effect_ref"] == effect_ref:
                    return
                raise ContractViolation("operation completion conflicts with durable operation state")
            self._event(row["work_order_id"], "operation_completed", actor, {"operationId": operation_id, "effectRef": effect_ref})

    def reconcile(
        self,
        operation_id: str,
        observed_effect_ref: str | None,
        evidence: str,
        actor: str,
    ) -> str:
        row = self._operation(operation_id)
        work = self.load(row["work_order_id"])
        if actor not in {work.document["releaseOwner"], work.document["recovery"]["owner"]}:
            raise ContractViolation("reconciliation requires release or recovery owner")
        if row["status"] in {"COMPLETED", "RECONCILED"}:
            return row["status"]
        if row["status"] != "INDETERMINATE":
            raise ContractViolation("reconciliation requires an indeterminate operation")
        if observed_effect_ref is None:
            with self.db:
                self._event(row["work_order_id"], "reconciliation_unresolved", actor, {"operationId": operation_id, "evidence": evidence})
            return "INDETERMINATE"
        with self.db:
            self.db.execute(
                "UPDATE operations SET status='RECONCILED', effect_ref=?, reconciliation_evidence=?, updated_at=? WHERE operation_id=?",
                (observed_effect_ref, evidence, _now(), operation_id),
            )
            self._event(row["work_order_id"], "operation_reconciled", actor, {"operationId": operation_id, "effectRef": observed_effect_ref, "evidence": evidence})
        return "RECONCILED"

    def create_receipt(
        self,
        work_order_id: str,
        digest: str,
        operation_id: str,
        actor: str,
        authority_used: list[str],
        release_mode: str,
        exposure: str,
        rollback: str,
        receipt_id: str | None = None,
    ) -> dict[str, Any]:
        work = self.load(work_order_id)
        if work.state != "RELEASING" or actor != work.document["releaseOwner"]:
            raise ContractViolation("receipt requires RELEASING state and release owner")
        operation = self._operation(operation_id)
        if operation["work_order_id"] != work.id or operation["status"] not in {"COMPLETED", "RECONCILED"}:
            raise ContractViolation("receipt requires a known or reconciled effect")
        current_digest = self.db.execute(
            "SELECT candidate_digest FROM work_orders WHERE id=?", (work.id,)
        ).fetchone()[0]
        if digest != current_digest:
            raise ContractViolation("receipt does not name the released candidate")
        for item in authority_used:
            if ":" not in item:
                raise ContractViolation("authorityUsed entries must be dimension:value")
            dimension, value = item.split(":", 1)
            try:
                self.policy.assert_authority(work.document, dimension, value)
            except PolicyViolation as exc:
                raise ContractViolation(str(exc)) from exc
        disposition = self.db.execute(
            "SELECT * FROM dispositions WHERE work_order_id=? AND candidate_digest=? ORDER BY created_at DESC LIMIT 1",
            (work.id, digest),
        ).fetchone()
        if disposition is None or disposition["decision"] not in {"approve", "exception"}:
            raise ContractViolation("receipt requires an approving disposition")
        evidence_ids = [
            row[0] for row in self.db.execute(
                "SELECT id FROM evidence_records WHERE work_order_id=? AND candidate_digest=? ORDER BY created_at,id",
                (work.id, digest),
            )
        ]
        operation_state = "reconciled" if operation["status"] == "RECONCILED" else "known-succeeded"
        document = {
            "schemaVersion": "1.0",
            "kind": "FactoryReceipt",
            "id": receipt_id or f"RC-{uuid.uuid4()}",
            "workOrderId": work.id,
            "intentVersion": work.document["version"],
            "candidateDigest": digest,
            "authorityUsed": authority_used,
            "evidenceRecordIds": evidence_ids,
            "disposition": {
                "actorId": disposition["actor_id"],
                "decision": disposition["decision"],
                "reason": disposition["reason"],
                "expiresAt": disposition["expires_at"],
            },
            "operation": {
                "id": operation_id,
                "state": operation_state,
                "reconciliationEvidence": operation["reconciliation_evidence"],
            },
            "release": {
                "actorId": actor,
                "mode": release_mode,
                "exposure": exposure,
                "rollback": rollback,
            },
            "recoveryOwner": work.document["recovery"]["owner"],
            "createdAt": _now(),
        }
        try:
            require_valid(document)
        except ArtifactError as exc:
            raise ContractViolation(str(exc)) from exc
        with self.db:
            self.db.execute(
                "INSERT INTO receipts VALUES (?,?,?,?,?)",
                (document["id"], work.id, operation_id, json.dumps(document, sort_keys=True), _now()),
            )
            self._event(work.id, "receipt_created", actor, {"id": document["id"]})
            self._transition_locked(work, "RELEASED", actor)
        return document

    def begin_observation(self, work_order_id: str, actor: str) -> WorkOrder:
        work = self.load(work_order_id)
        if actor != work.document["consequenceOwner"]:
            raise ContractViolation("observation requires consequence owner")
        return self._transition(work.id, work.version, "OBSERVING", actor)

    def record_outcome(self, document: dict[str, Any], actor: str) -> WorkOrder:
        try:
            require_valid(document)
        except ArtifactError as exc:
            raise ContractViolation(str(exc)) from exc
        if document["kind"] != "OutcomeObservation":
            raise ContractViolation("record_outcome requires an OutcomeObservation")
        receipt = self.db.execute(
            "SELECT work_order_id FROM receipts WHERE id=?", (document["receiptId"],)
        ).fetchone()
        if receipt is None:
            raise ContractViolation("outcome references an unknown receipt")
        work = self.load(receipt[0])
        if work.state != "OBSERVING" or actor != work.document["consequenceOwner"] or document["decisionOwner"] != actor:
            raise ContractViolation("outcome requires OBSERVING state and consequence owner")
        if document["disposition"] == "not-yet-due":
            target = None
        else:
            target = {
                "effective": "EFFECTIVE", "ineffective": "INEFFECTIVE",
                "insufficient": "INSUFFICIENT", "harmful": "HARMFUL",
            }[document["disposition"]]
        with self.db:
            self.db.execute(
                "INSERT INTO outcomes VALUES (?,?,?,?)",
                (document["id"], document["receiptId"], json.dumps(document, sort_keys=True), _now()),
            )
            self._event(work.id, "outcome_recorded", actor, {"id": document["id"], "disposition": document["disposition"]})
            if target:
                self._transition_locked(work, target, actor)
        return self.load(work.id)

    def propose_learning(
        self, work_order_id: str, learning_id: str, claim: str, scope: dict[str, Any], actor: str
    ) -> None:
        self.load(work_order_id)
        with self.db:
            self.db.execute(
                "INSERT INTO learnings VALUES (?,?, 'CANDIDATE', ?, ?, '[]', NULL, ?)",
                (learning_id, work_order_id, claim, json.dumps(scope, sort_keys=True), _now()),
            )
            self._event(work_order_id, "learning_proposed", actor, {"id": learning_id})

    def promote_learning(
        self,
        learning_id: str,
        evidence_ids: list[str],
        expires_at: str,
        actor: str,
        changes_protected_policy: bool = False,
    ) -> None:
        row = self.db.execute("SELECT * FROM learnings WHERE id=?", (learning_id,)).fetchone()
        if row is None:
            raise KeyError(learning_id)
        work = self.load(row["work_order_id"])
        if actor != work.document["learningOwner"]:
            raise ContractViolation("learning promotion requires the learning owner")
        if row["state"] != "CANDIDATE" or not evidence_ids or not expires_at:
            raise ContractViolation("learning promotion requires candidate state, evidence, and expiry")
        if changes_protected_policy:
            raise ContractViolation("improvement cannot change its own protected policy or judge")
        known_ids = {
            item[0] for table in ("evidence_records", "receipts", "outcomes")
            for item in self.db.execute(f"SELECT id FROM {table}")
        }
        if any(item not in known_ids for item in evidence_ids):
            raise ContractViolation("learning evidence must reference durable evidence, receipt, or outcome records")
        with self.db:
            self.db.execute(
                "UPDATE learnings SET state='VALIDATED', evidence_json=?, expires_at=?, updated_at=? WHERE id=?",
                (json.dumps(evidence_ids), expires_at, _now(), learning_id),
            )
            self._event(work.id, "learning_validated", actor, {"id": learning_id, "evidence": evidence_ids, "expiresAt": expires_at})

    def retire_learning(self, learning_id: str, actor: str, reason: str) -> None:
        row = self.db.execute("SELECT * FROM learnings WHERE id=?", (learning_id,)).fetchone()
        if row is None:
            raise KeyError(learning_id)
        work = self.load(row["work_order_id"])
        if actor != work.document["learningOwner"]:
            raise ContractViolation("learning retirement requires the learning owner")
        with self.db:
            self.db.execute(
                "UPDATE learnings SET state='RETIRED', updated_at=? WHERE id=?",
                (_now(), learning_id),
            )
            self._event(work.id, "learning_retired", actor, {"id": learning_id, "reason": reason})

    def learning_can_influence(
        self, learning_id: str, scope: dict[str, Any], now: str
    ) -> bool:
        row = self.db.execute("SELECT * FROM learnings WHERE id=?", (learning_id,)).fetchone()
        return bool(
            row
            and row["state"] == "VALIDATED"
            and row["expires_at"] > now
            and json.loads(row["scope_json"]) == scope
        )

    def events(self, work_order_id: str) -> list[dict[str, Any]]:
        rows = self.db.execute(
            "SELECT seq,kind,actor_id,body_json,created_at FROM events WHERE work_order_id=? ORDER BY seq",
            (work_order_id,),
        )
        return [
            {
                "seq": row["seq"], "kind": row["kind"], "actorId": row["actor_id"],
                "body": json.loads(row["body_json"]), "createdAt": row["created_at"],
            }
            for row in rows
        ]

    def trace(self, work_order_id: str) -> dict[str, Any]:
        work = self.load(work_order_id)
        def documents(table: str, key: str = "work_order_id") -> list[dict[str, Any]]:
            return [
                json.loads(row[0]) for row in self.db.execute(
                    f"SELECT document_json FROM {table} WHERE {key}=? ORDER BY created_at",
                    (work_order_id,),
                )
            ]
        receipts = documents("receipts")
        outcomes: list[dict[str, Any]] = []
        for receipt in receipts:
            outcomes.extend(
                json.loads(row[0]) for row in self.db.execute(
                    "SELECT document_json FROM outcomes WHERE receipt_id=? ORDER BY created_at",
                    (receipt["id"],),
                )
            )
        dispositions = [dict(row) for row in self.db.execute(
            "SELECT id,candidate_digest,actor_id,decision,reason,expires_at,created_at FROM dispositions WHERE work_order_id=? ORDER BY created_at,id",
            (work_order_id,),
        )]
        operations = [dict(row) for row in self.db.execute(
            "SELECT operation_id,status,effect_ref,reconciliation_evidence,updated_at FROM operations WHERE work_order_id=? ORDER BY updated_at,operation_id",
            (work_order_id,),
        )]
        attempts = [dict(row) for row in self.db.execute(
            "SELECT id,parent_id,kind,state,reserved_units,result_json,created_at FROM attempts WHERE work_order_id=? ORDER BY created_at,id",
            (work_order_id,),
        )]
        leases = [dict(row) for row in self.db.execute(
            "SELECT holder,expires_at,epoch,updated_at FROM leases WHERE work_order_id=?", (work_order_id,),
        )]
        learnings = [dict(row) for row in self.db.execute(
            "SELECT id,state,claim,scope_json,evidence_json,expires_at,updated_at FROM learnings WHERE work_order_id=? ORDER BY updated_at,id",
            (work_order_id,),
        )]
        return {
            "workOrder": work.document,
            "state": work.state,
            "version": work.version,
            "events": self.events(work_order_id),
            "evidence": documents("evidence_records"),
            "dispositions": dispositions,
            "operations": operations,
            "attempts": attempts,
            "leases": leases,
            "receipts": receipts,
            "outcomes": outcomes,
            "learnings": learnings,
        }

    def metrics(self) -> dict[str, Any]:
        states = {
            row[0]: row[1]
            for row in self.db.execute("SELECT state,count(*) FROM work_orders GROUP BY state")
        }
        return {
            "workOrdersByState": states,
            "evidenceRecords": self.db.execute("SELECT count(*) FROM evidence_records").fetchone()[0],
            "indeterminateOperations": self.db.execute("SELECT count(*) FROM operations WHERE status='INDETERMINATE'").fetchone()[0],
            "receipts": self.db.execute("SELECT count(*) FROM receipts").fetchone()[0],
            "outcomes": self.db.execute("SELECT count(*) FROM outcomes").fetchone()[0],
        }

    def _operation(self, operation_id: str) -> sqlite3.Row:
        row = self.db.execute(
            "SELECT * FROM operations WHERE operation_id=?", (operation_id,)
        ).fetchone()
        if row is None:
            raise KeyError(operation_id)
        return row

    def _event(
        self, work_order_id: str, kind: str, actor: str, body: dict[str, Any]
    ) -> None:
        self.db.execute(
            "INSERT INTO events(work_order_id,kind,actor_id,body_json,created_at) VALUES (?,?,?,?,?)",
            (work_order_id, kind, actor, json.dumps(body, sort_keys=True), _now()),
        )
