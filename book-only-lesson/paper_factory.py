"""Local teaching boundary. Role labels are NOT authentication."""
import hashlib
import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path


def encode(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value):
    return hashlib.sha256(encode(value).encode()).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


class Factory:

    def __init__(self, directory):
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(directory / "factory.sqlite")
        self.target = sqlite3.connect(directory / "target.sqlite")
        self.db.execute("CREATE TABLE IF NOT EXISTS history "
                        "(version INTEGER PRIMARY KEY, body TEXT)")
        self.target.execute("CREATE TABLE IF NOT EXISTS effects "
                            "(key TEXT PRIMARY KEY, body TEXT)")
        self.db.commit()
        self.target.commit()

    def close(self):
        self.db.close()
        self.target.close()

    def read(self):
        row = self.db.execute(
            "SELECT body FROM history ORDER BY version DESC LIMIT 1"
        ).fetchone()
        return json.loads(row[0]) if row else {"version": 0}

    @contextmanager
    def change(self, expected, actor):
        # Reserve the writer before reading: stale writers cannot race.
        self.db.execute("BEGIN IMMEDIATE")
        try:
            state = self.read()
            require(state["version"] == expected, "stale version")
            yield state
            state["version"] += 1
            state["actor"] = actor
            state["schema"] = 1
            state["scope"] = "Meridian teaching sandbox"
            state["at"] = datetime.now(timezone.utc).isoformat()
            self.db.execute("INSERT INTO history VALUES (?, ?)",
                            (state["version"], encode(state)))
            self.db.commit()
        except BaseException:
            self.db.rollback()
            raise

    def admit(self, expected, actor, request):
        with self.change(expected, actor) as s:
            require(actor == "owner", "owner required")
            require(expected == 0, "one work order per directory")
            require(request == "round cents, sandbox only",
                    "ineligible intent")
            s.update(work={"id": "WO-1", "intent": request,
                           "owner": actor, "policy": "teaching-1",
                           "criterion": "1.005 becomes 1.01; half up",
                           "prohibition": "no production release",
                           "outcome": "error=harm; n<100=insufficient"},
                     stage="admitted", release_grant=True, attempts=0)

    def attempt(self, expected, actor):
        with self.change(expected, actor) as s:
            require(actor == "producer", "producer required")
            require(s.get("stage") == "admitted", "not admitted")
            require(s["attempts"] < 3, "attempt budget exhausted")
            s["attempts"] += 1
            s.update(stage="running", attempt={
                "id": "A-" + str(s["attempts"]),
                "work_version": expected, "actor": actor,
                "scope": "sandbox", "total_attempt_budget": 3})

    def candidate(self, expected, actor, mode):
        with self.change(expected, actor) as s:
            require(actor == "producer", "producer required")
            require(s.get("stage") == "running", "not running")
            require(mode in ("half_even", "half_up"), "unknown mode")
            artifact = {"rounding": mode, "scope": "sandbox"}
            s.update(stage="candidate", candidate={
                "attempt": s["attempt"]["id"], "artifact": artifact,
                "digest": digest(artifact), "producer": actor})

    def evaluate(self, expected, actor, claimed_digest):
        from decimal import Decimal, ROUND_HALF_EVEN, ROUND_HALF_UP
        with self.change(expected, actor) as s:
            require(actor == "evaluator", "evaluator required")
            require(s.get("stage") == "candidate", "no candidate")
            c = s["candidate"]
            require(c["digest"] == claimed_digest, "wrong candidate")
            mode = c["artifact"]["rounding"]
            rule = (ROUND_HALF_UP if mode == "half_up"
                    else ROUND_HALF_EVEN)
            actual = str(Decimal("1.005").quantize(
                Decimal("0.01"), rounding=rule))
            s.update(stage="evaluated", verdict={
                "digest": claimed_digest, "criterion": "cents-1",
                "source": "decimal fixture v1", "input": "1.005",
                "expected": "1.01", "actual": actual,
                "result": "pass" if actual == "1.01" else "fail",
                "limit": "one fixture is not complete testing"})

    def decide(self, expected, actor, choice, why):
        with self.change(expected, actor) as s:
            require(actor == "reviewer", "reviewer required")
            require(s.get("stage") == "evaluated", "not evaluated")
            require(choice in ("approve", "reject"), "bad choice")
            require(bool(why.strip()), "rationale required")
            v, c = s["verdict"], s["candidate"]
            require(v["digest"] == c["digest"], "stale evidence")
            if choice == "approve":
                require(v["result"] == "pass", "blocking failure")
            s.update(stage=choice, decision={
                "actor": actor, "choice": choice, "why": why,
                "digest": c["digest"], "policy": "teaching-1",
                "evidence_version": expected})

    def revise(self, expected, actor, why):
        with self.change(expected, actor) as s:
            require(actor == "reviewer", "reviewer required")
            require(s.get("stage") in ("evaluated", "approve"),
                    "not revisable")
            require(bool(why.strip()), "rationale required")
            s["revision"] = {"actor": actor, "why": why,
                             "prior_digest": s["candidate"]["digest"]}
            # Prior snapshots retain evidence; new work cannot use it.
            for name in ("candidate", "verdict", "decision", "attempt"):
                s.pop(name, None)
            s["stage"] = "admitted"

    def revoke(self, expected, actor):
        with self.change(expected, actor) as s:
            require(actor == "owner", "owner required")
            require("work" in s, "no work order")
            s["release_grant"] = False

    def prepare(self, expected, actor, key):
        with self.change(expected, actor) as s:
            require(actor == "releaser", "releaser required")
            require(s.get("stage") == "approve", "not approved")
            require(s["release_grant"], "grant revoked")
            require(bool(key.strip()), "operation key required")
            c = s["candidate"]
            require(s["decision"]["digest"] == c["digest"],
                    "stale approval")
            s.update(stage="indeterminate", effect={
                "key": key, "digest": c["digest"],
                "artifact": c["artifact"], "target": "sandbox"})

    def target_apply(self, effect):
        # Separate target transaction: effect and key commit together.
        with self.target:
            self.target.execute("BEGIN IMMEDIATE")
            row = self.target.execute(
                "SELECT body FROM effects WHERE key=?",
                (effect["key"],)).fetchone()
            if row:
                require(row[0] == encode(effect), "key conflict")
            else:
                self.target.execute("INSERT INTO effects VALUES (?, ?)",
                                    (effect["key"], encode(effect)))

    def send(self, expected, actor, lose_reply=False):
        with self.change(expected, actor) as s:
            require(actor == "releaser", "releaser required")
            require(s.get("stage") == "indeterminate", "no intent")
            require(s["release_grant"], "grant revoked")
            self.target_apply(s["effect"])
            if lose_reply:
                # Rolls back only factory transaction. Target committed.
                raise TimeoutError("reply lost; effect unknown locally")
            s.update(stage="released", receipt={
                "key": s["effect"]["key"], "status": "completed",
                "digest": s["effect"]["digest"], "via": "response"})

    def reconcile(self, expected, actor):
        with self.change(expected, actor) as s:
            require(actor == "operator", "operator required")
            require(s.get("stage") == "indeterminate", "no unknown")
            e = s["effect"]
            row = self.target.execute(
                "SELECT body FROM effects WHERE key=?",
                (e["key"],)).fetchone()
            require(row is not None, "no receipt: retain uncertainty")
            require(row[0] == encode(e), "key conflict: escalate")
            # Observing an old effect does not authorize a new effect.
            s.update(stage="released", receipt={
                "key": e["key"], "status": "completed",
                "digest": e["digest"], "via": "target query"})

    def observe(self, expected, actor, sample, errors):
        with self.change(expected, actor) as s:
            require(actor == "outcome-owner", "outcome owner required")
            require(s.get("stage") == "released", "not released")
            require(type(sample) is int and type(errors) is int,
                    "integer counts required")
            require(0 <= errors <= sample, "invalid counts")
            result = ("harmful" if errors else
                      "insufficient" if sample < 100 else "effective")
            s.update(stage="observed", outcome={
                "release": s["receipt"]["key"], "sample": sample,
                "errors": errors, "result": result,
                "window": "synthetic one-day sandbox observation",
                "limit": "fixture counts; no business-value proof"})

    def propose(self, expected, actor, text):
        with self.change(expected, actor) as s:
            require(actor == "analyst", "analyst required")
            require(s.get("stage") == "observed", "no observation")
            require(bool(text.strip()), "proposal required")
            s.update(stage="proposal", learning={
                "source_version": expected, "text": text,
                "status": "proposed", "authority": "none"})
