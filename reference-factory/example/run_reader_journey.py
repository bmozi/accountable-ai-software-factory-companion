#!/usr/bin/env python3
"""Run a complete, offline Meridian Ledger accountability journey.

© 2026 John Briggs — MIT licensed; see ../../LICENSE-CODE.
"""

from __future__ import annotations

import copy
import json
import tempfile
from pathlib import Path

from accountable_factory import Factory, PolicyEngine
from accountable_factory.adapters import DeterministicProducer, LocalGitAdapter, LostResponse


ROOT = Path(__file__).resolve().parents[2]


def evidence(work: dict, digest: str, criterion: str, suffix: str) -> dict:
    return {
        "schemaVersion": "1.0", "kind": "EvidenceRecord",
        "id": f"EV-JOURNEY-{suffix}", "workOrderId": work["id"],
        "candidateDigest": digest, "criterionId": criterion,
        "producerId": work["producerId"],
        "evaluator": {"actorId": "contract-evaluator-02", "type": "deterministic", "independence": "separate-method"},
        "method": f"Offline check for {criterion}", "result": "pass",
        "decisive": True, "observedAt": "2026-08-23T12:00:00Z",
        "limitations": ["Fictional, local teaching journey"],
    }


def run(database: Path, effect_repository: Path) -> dict:
    work = json.loads((ROOT / "examples/artifacts/work-order.valid.json").read_text())
    factory = Factory(database, PolicyEngine.from_file(ROOT / "policies/default-policy.json"))
    factory.admit(work, work["owner"])
    running = factory.start(work["id"], work["version"], work["owner"])
    factory.create_attempt(work["id"], "ATT-JOURNEY-01", work["producerId"], 4)
    factory.assert_capability(work["id"], "tools", "repository-read", work["producerId"])
    candidate = DeterministicProducer("offline-reference-provider").produce(work)
    digest = factory.record_candidate(work["id"], running.version, candidate, work["producerId"])
    factory.complete_attempt("ATT-JOURNEY-01", work["producerId"], {"candidateDigest": digest})
    factory.begin_verification(work["id"], "contract-evaluator-02")
    for number, criterion in enumerate(work["evidenceFloor"], start=1):
        factory.record_evidence(evidence(work, digest, criterion, f"{number:02d}"), "contract-evaluator-02")
    factory.request_decision(work["id"], digest, "contract-evaluator-02")
    factory.decide(work["id"], digest, work["consequenceOwner"], "approve", "Declared evidence floor passed")

    operation_id = "OP-JOURNEY-CANARY-001"
    factory.begin_release(work["id"], operation_id, work["releaseOwner"])
    adapter = LocalGitAdapter(effect_repository)
    try:
        adapter.publish(operation_id, candidate, lose_response=True)
    except LostResponse:
        factory.mark_indeterminate(operation_id, work["releaseOwner"])
    observed = adapter.observe(operation_id)
    factory.reconcile(operation_id, observed, "Git tag proves exactly one local effect", work["releaseOwner"])
    receipt = factory.create_receipt(
        work["id"], digest, operation_id, work["releaseOwner"],
        ["tools:repository-read", "writes:isolated-workspace"],
        "canary", "one local teaching repository", "delete local tag and commit",
        "RC-JOURNEY-001",
    )
    factory.begin_observation(work["id"], work["consequenceOwner"])
    outcome = copy.deepcopy(json.loads((ROOT / "examples/artifacts/outcome.valid.json").read_text()))
    outcome.update({"id": "OUT-JOURNEY-001", "receiptId": receipt["id"]})
    factory.record_outcome(outcome, work["consequenceOwner"])
    factory.propose_learning(work["id"], "LRN-JOURNEY-001", "Reconcile local Git effects by semantic tag", {"workClass": work["workClass"]}, work["learningOwner"])
    factory.promote_learning("LRN-JOURNEY-001", [receipt["id"], outcome["id"]], "2026-12-31T00:00:00Z", work["learningOwner"])
    result = {"trace": factory.trace(work["id"]), "metrics": factory.metrics(), "effectCount": adapter.effect_count(operation_id)}
    factory.close()
    return result


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="accountable-factory-") as temp:
        root = Path(temp)
        result = run(root / "factory.db", root / "effect-repository")
        print(json.dumps(result, indent=2, sort_keys=True))
        assert result["effectCount"] == 1
        assert result["trace"]["state"] == "INSUFFICIENT"
        print("Journey complete: one effect, durable evidence, receipt, outcome, and governed learning.")


if __name__ == "__main__":
    main()
