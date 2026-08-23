"""Executable proof of all twenty-four published acceptance obligations.

© 2026 John Briggs — MIT licensed; see ../../LICENSE-CODE.
"""

from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from accountable_factory import ContractViolation, Factory, PolicyEngine
from accountable_factory.adapters import DeterministicProducer, LocalGitAdapter, LostResponse


ROOT = Path(__file__).resolve().parents[2]


class AcceptanceObligations(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.database = self.root / "factory.db"
        self.work = json.loads((ROOT / "examples/artifacts/work-order.valid.json").read_text())
        self.factory = Factory(self.database, PolicyEngine.from_file(ROOT / "policies/default-policy.json"))

    def tearDown(self) -> None:
        try:
            self.factory.close()
        except Exception:
            pass
        self.temp.cleanup()

    def admit(self) -> None:
        self.factory.admit(self.work, self.work["owner"])

    def candidate(self, content: bytes = b"candidate-v1") -> str:
        self.admit()
        running = self.factory.start(self.work["id"], self.work["version"], self.work["owner"])
        return self.factory.record_candidate(self.work["id"], running.version, content, self.work["producerId"])

    def evidence(self, digest: str, criterion: str, result: str = "pass", actor: str = "evaluator-01", decisive: bool = True, suffix: str = "01") -> dict:
        return {
            "schemaVersion": "1.0", "kind": "EvidenceRecord", "id": f"EV-{suffix}",
            "workOrderId": self.work["id"], "candidateDigest": digest,
            "criterionId": criterion, "producerId": self.work["producerId"],
            "evaluator": {"actorId": actor, "type": "deterministic", "independence": "separate-method"},
            "method": "acceptance test", "result": result, "decisive": decisive,
            "observedAt": "2026-08-23T12:00:00Z", "limitations": ["teaching fixture"],
        }

    def to_decision(self, content: bytes = b"candidate-v1") -> str:
        digest = self.candidate(content)
        self.factory.begin_verification(self.work["id"], "evaluator-01")
        for number, criterion in enumerate(self.work["evidenceFloor"], 1):
            self.factory.record_evidence(self.evidence(digest, criterion, suffix=str(number)), "evaluator-01")
        self.factory.request_decision(self.work["id"], digest, "evaluator-01")
        return digest

    def approve(self) -> str:
        digest = self.to_decision()
        self.factory.decide(self.work["id"], digest, self.work["consequenceOwner"], "approve", "evidence passed")
        return digest

    def release(self) -> tuple[str, dict]:
        digest = self.approve()
        operation = "OP-ACCEPTANCE-001"
        self.factory.begin_release(self.work["id"], operation, self.work["releaseOwner"])
        self.factory.complete_operation(operation, "local-effect-001", self.work["releaseOwner"])
        receipt = self.factory.create_receipt(
            self.work["id"], digest, operation, self.work["releaseOwner"],
            ["tools:repository-read"], "canary", "teaching fixture", "delete fixture", "RC-ACCEPTANCE-001",
        )
        return digest, receipt

    def test_a01_ineligible_intent_is_refused_without_attempt(self) -> None:
        invalid = copy.deepcopy(self.work); del invalid["promise"]
        with self.assertRaises(ContractViolation): self.factory.admit(invalid, invalid["owner"])
        self.assertEqual(self.factory.db.execute("SELECT count(*) FROM attempts").fetchone()[0], 0)

    def test_a02_intent_update_versions_without_erasing_event(self) -> None:
        self.admit(); updated = copy.deepcopy(self.work); updated["version"] += 1; updated["promise"] += " clearly"
        result = self.factory.update_intent(self.work["id"], self.work["version"], updated, self.work["owner"])
        self.assertEqual(result.version, 4); self.assertEqual(self.factory.events(self.work["id"])[0]["body"]["version"], 3)

    def test_a03_stale_compare_and_set_has_no_partial_transition(self) -> None:
        self.admit(); self.factory.start(self.work["id"], 3, self.work["owner"])
        with self.assertRaisesRegex(ContractViolation, "stale"): self.factory.transition(self.work["id"], 3, "CANCELLED", self.work["owner"])
        self.assertEqual(self.factory.load(self.work["id"]).state, "RUNNING")

    def test_a04_prohibited_capability_is_denied_and_attributed(self) -> None:
        self.admit()
        with self.assertRaisesRegex(ContractViolation, "denied"): self.factory.assert_capability(self.work["id"], "writes", "production", self.work["producerId"])
        self.assertEqual(self.factory.events(self.work["id"])[-1]["kind"], "authority_denied")

    def test_a05_budget_cannot_expand_silently(self) -> None:
        self.admit(); self.factory.create_attempt(self.work["id"], "A", self.work["producerId"], 10)
        with self.assertRaisesRegex(ContractViolation, "budget"): self.factory.create_attempt(self.work["id"], "B", self.work["producerId"], 1)

    def test_a06_revocation_denies_next_protected_operation(self) -> None:
        self.admit(); self.factory.revoke_capability(self.work["id"], "tools", "repository-read", self.work["owner"])
        with self.assertRaisesRegex(ContractViolation, "revoked"): self.factory.assert_capability(self.work["id"], "tools", "repository-read", self.work["producerId"])

    def test_a07_producer_claim_cannot_be_decisive(self) -> None:
        digest = self.candidate(); self.factory.begin_verification(self.work["id"], self.work["producerId"])
        claim = self.evidence(digest, self.work["evidenceFloor"][0], actor=self.work["producerId"], decisive=False)
        self.factory.record_evidence(claim, self.work["producerId"])
        self.assertEqual(self.factory.evidence_status(self.work["id"], digest, self.work["evidenceFloor"][0]), "missing")
        decisive = copy.deepcopy(claim); decisive["id"] = "EV-DECISIVE"; decisive["decisive"] = True
        with self.assertRaises(ContractViolation): self.factory.record_evidence(decisive, self.work["producerId"])

    def test_a08_new_candidate_invalidates_old_artifact_evidence(self) -> None:
        digest = self.candidate(); self.factory.begin_verification(self.work["id"], "evaluator-01")
        for number, criterion in enumerate(self.work["evidenceFloor"], 1): self.factory.record_evidence(self.evidence(digest, criterion, suffix=str(number)), "evaluator-01")
        self.factory.request_decision(self.work["id"], digest, "evaluator-01"); repaired = self.factory.decide(self.work["id"], digest, self.work["consequenceOwner"], "repair", "change needed")
        replacement = self.factory.record_candidate(self.work["id"], repaired.version, b"candidate-v2", self.work["producerId"])
        self.assertFalse(self.factory.evidence_satisfies(self.work["id"], replacement, self.work["evidenceFloor"]))
        self.factory.begin_verification(self.work["id"], "evaluator-01")
        with self.assertRaisesRegex(ContractViolation, "current candidate"): self.factory.request_decision(self.work["id"], digest, "evaluator-01")

    def test_a09_conflicting_evidence_remains_unresolved(self) -> None:
        digest = self.candidate(); self.factory.begin_verification(self.work["id"], "evaluator-01"); criterion = self.work["evidenceFloor"][0]
        self.factory.record_evidence(self.evidence(digest, criterion, "pass", suffix="pass"), "evaluator-01")
        self.factory.record_evidence(self.evidence(digest, criterion, "fail", actor="evaluator-02", suffix="fail"), "evaluator-02")
        self.assertEqual(self.factory.evidence_status(self.work["id"], digest, criterion), "conflict")

    def test_a10_illegal_state_transition_is_rejected(self) -> None:
        self.admit()
        with self.assertRaisesRegex(ContractViolation, "illegal"): self.factory.transition(self.work["id"], 3, "APPROVED", self.work["owner"])

    def test_a11_exception_requires_independent_owner_and_expiry(self) -> None:
        digest = self.to_decision()
        with self.assertRaises(ContractViolation): self.factory.decide(self.work["id"], digest, self.work["producerId"], "exception", "risk accepted", "2026-09-01Z")
        with self.assertRaisesRegex(ContractViolation, "expiry"): self.factory.decide(self.work["id"], digest, self.work["consequenceOwner"], "exception", "risk accepted")

    def test_a12_lost_response_reconciles_to_one_effect(self) -> None:
        digest = self.approve(); operation = "OP-LOST"; self.factory.begin_release(self.work["id"], operation, self.work["releaseOwner"]); adapter = LocalGitAdapter(self.root / "effect")
        with self.assertRaises(LostResponse): adapter.publish(operation, b"candidate", lose_response=True)
        self.factory.mark_indeterminate(operation, self.work["releaseOwner"]); self.factory.reconcile(operation, adapter.observe(operation), "tag observed", self.work["releaseOwner"])
        self.assertEqual(adapter.effect_count(operation), 1)

    def test_a13_duplicate_operation_identity_creates_no_duplicate(self) -> None:
        self.approve(); operation = "OP-ONE"; self.factory.begin_release(self.work["id"], operation, self.work["releaseOwner"])
        with self.assertRaises(ContractViolation): self.factory.begin_release(self.work["id"], operation, self.work["releaseOwner"])
        self.assertEqual(self.factory.db.execute("SELECT count(*) FROM operations WHERE operation_id=?", (operation,)).fetchone()[0], 1)

    def test_a14_expired_lease_recovers_from_durable_epoch(self) -> None:
        self.admit(); self.assertEqual(self.factory.acquire_lease(self.work["id"], self.work["producerId"], "2026-08-23T10:00:00Z", "2026-08-23T11:00:00Z"), 1)
        with self.assertRaises(ContractViolation): self.factory.acquire_lease(self.work["id"], self.work["releaseOwner"], "2026-08-23T10:30:00Z", "2026-08-23T12:00:00Z")
        self.assertEqual(self.factory.acquire_lease(self.work["id"], self.work["releaseOwner"], "2026-08-23T11:01:00Z", "2026-08-23T12:00:00Z"), 2)

    def test_a15_release_without_disposition_is_blocked(self) -> None:
        self.candidate()
        with self.assertRaises(ContractViolation): self.factory.begin_release(self.work["id"], "OP-NO-DISPOSITION", self.work["releaseOwner"])

    def test_a16_harmful_countermetric_exposes_rollback_path(self) -> None:
        _, receipt = self.release(); self.factory.begin_observation(self.work["id"], self.work["consequenceOwner"]); outcome = self.outcome(receipt["id"], "harmful")
        state = self.factory.record_outcome(outcome, self.work["consequenceOwner"]); self.assertEqual(state.state, "HARMFUL")
        state = self.factory.transition(self.work["id"], state.version, "ROLLED_BACK", self.work["consequenceOwner"]); self.assertEqual(state.state, "ROLLED_BACK")

    def test_a17_weak_observation_is_insufficient_not_success(self) -> None:
        _, receipt = self.release(); self.factory.begin_observation(self.work["id"], self.work["consequenceOwner"])
        state = self.factory.record_outcome(self.outcome(receipt["id"], "insufficient"), self.work["consequenceOwner"]); self.assertEqual(state.state, "INSUFFICIENT")

    def test_a18_parent_cancellation_stops_children_and_late_results(self) -> None:
        self.admit(); self.factory.create_attempt(self.work["id"], "P", self.work["producerId"], 8); self.factory.create_attempt(self.work["id"], "C", self.work["producerId"], 4, "child", "P"); self.factory.cancel_attempt("P", self.work["owner"])
        with self.assertRaisesRegex(ContractViolation, "late"): self.factory.complete_attempt("C", self.work["producerId"], {"result": "late"})

    def test_a19_child_budget_is_conserved_under_parent(self) -> None:
        self.admit(); self.factory.create_attempt(self.work["id"], "P", self.work["producerId"], 5); self.factory.create_attempt(self.work["id"], "C1", self.work["producerId"], 4, "child", "P")
        with self.assertRaisesRegex(ContractViolation, "exceed"): self.factory.create_attempt(self.work["id"], "C2", self.work["producerId"], 2, "child", "P")

    def test_a20_single_case_learning_has_no_immediate_influence(self) -> None:
        self.admit(); scope = {"workClass": self.work["workClass"]}; self.factory.propose_learning(self.work["id"], "L1", "one case", scope, self.work["learningOwner"])
        self.assertFalse(self.factory.learning_can_influence("L1", scope, "2026-08-23T00:00:00Z"))

    def test_a21_learning_cannot_weaken_its_protected_judge(self) -> None:
        self.admit(); self.factory.propose_learning(self.work["id"], "L1", "weaken judge", {}, self.work["learningOwner"])
        with self.assertRaisesRegex(ContractViolation, "protected"): self.factory.promote_learning("L1", ["EV-1"], "2027-01-01Z", self.work["learningOwner"], True)

    def test_a22_retired_learning_loses_influence_but_history_remains(self) -> None:
        self.to_decision(); scope = {"workClass": self.work["workClass"]}; self.factory.propose_learning(self.work["id"], "L1", "bounded claim", scope, self.work["learningOwner"]); self.factory.promote_learning("L1", ["EV-1"], "2027-01-01Z", self.work["learningOwner"])
        self.assertTrue(self.factory.learning_can_influence("L1", scope, "2026-09-01Z")); self.factory.retire_learning("L1", self.work["learningOwner"], "contradicted")
        self.assertFalse(self.factory.learning_can_influence("L1", scope, "2026-09-01Z")); self.assertIn("learning_retired", [event["kind"] for event in self.factory.events(self.work["id"])])

    def test_a23_provider_replacement_preserves_domain_contract(self) -> None:
        first = DeterministicProducer("provider-a").produce(self.work); second = DeterministicProducer("provider-b").produce(self.work)
        self.assertNotEqual(first, second); self.assertEqual(json.loads(first)["workOrderId"], json.loads(second)["workOrderId"])

    def test_a24_trace_reconstructs_completion_without_chat_history(self) -> None:
        _, receipt = self.release(); self.factory.begin_observation(self.work["id"], self.work["consequenceOwner"]); self.factory.record_outcome(self.outcome(receipt["id"], "insufficient"), self.work["consequenceOwner"])
        trace = self.factory.trace(self.work["id"])
        self.assertTrue(all(trace[key] for key in ("workOrder", "events", "evidence", "dispositions", "operations", "receipts", "outcomes"))); self.assertEqual(trace["state"], "INSUFFICIENT")

    def outcome(self, receipt_id: str, disposition: str) -> dict:
        return {
            "schemaVersion": "1.0", "kind": "OutcomeObservation", "id": f"OUT-{disposition}", "receiptId": receipt_id,
            "observedAt": "2026-09-05T18:30:00Z", "window": "fourteen-day canary",
            "primaryMeasure": {"name": "cycle time", "value": 11, "baseline": 16},
            "countermetrics": [{"name": "harm", "value": 1 if disposition == "harmful" else 0}],
            "denominator": 37, "limitations": ["teaching fixture"], "disposition": disposition,
            "decisionOwner": self.work["consequenceOwner"],
        }


if __name__ == "__main__":
    unittest.main()
