import tempfile
import unittest
from pathlib import Path

from reference_factory import ContractViolation, Factory


INTENT = {
    "promise": "upgrade one patch dependency",
    "criteria": ["tests", "policy"],
    "prohibitions": ["no release", "no unrelated upgrade"],
    "owner": "work-class-owner",
}


class ReferenceFactoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / "factory.db"
        self.factory = Factory(self.path)

    def tearDown(self):
        self.factory.db.close()
        self.temp.cleanup()

    def test_refuses_incomplete_intent(self):
        with self.assertRaises(ContractViolation):
            self.factory.admit({"promise": "do something"})

    def test_compare_and_set_rejects_stale_transition(self):
        work = self.factory.admit(INTENT)
        self.factory.transition(work.id, work.version, "RUNNING", "operator")
        with self.assertRaisesRegex(ContractViolation, "stale"):
            self.factory.transition(work.id, work.version, "CANCELLED", "operator")

    def test_producer_cannot_author_decisive_verdict(self):
        work = self.factory.admit(INTENT)
        running = self.factory.transition(work.id, work.version, "RUNNING", "operator")
        digest = self.factory.record_candidate(work.id, running.version, b"candidate")
        with self.assertRaisesRegex(ContractViolation, "producer"):
            self.factory.verdict(digest, "tests", "same-producer", "pass", producer=True)

    def test_evidence_is_bound_to_candidate_digest(self):
        work = self.factory.admit(INTENT)
        running = self.factory.transition(work.id, work.version, "RUNNING", "operator")
        first = self.factory.record_candidate(work.id, running.version, b"candidate-one")
        second = self.factory.record_candidate(work.id, running.version, b"candidate-two")
        self.factory.verdict(first, "tests", "ci", "pass")
        self.assertTrue(self.factory.evidence_satisfies(first, ["tests"]))
        self.assertFalse(self.factory.evidence_satisfies(second, ["tests"]))

    def test_conflicting_evidence_cannot_be_hidden_by_one_pass(self):
        work = self.factory.admit(INTENT)
        running = self.factory.transition(work.id, work.version, "RUNNING", "operator")
        digest = self.factory.record_candidate(work.id, running.version, b"candidate")
        self.factory.verdict(digest, "tests", "evaluator-a", "pass")
        self.factory.verdict(digest, "tests", "evaluator-b", "fail")
        self.assertEqual(self.factory.evidence_status(digest, "tests"), "conflict")
        self.assertFalse(self.factory.evidence_satisfies(digest, ["tests"]))

    def test_duplicate_operation_id_is_one_durable_operation(self):
        work = self.factory.admit(INTENT)
        self.factory.begin_operation(work.id, "release-123")
        self.factory.begin_operation(work.id, "release-123")
        count = self.factory.db.execute(
            "SELECT count(*) FROM operations WHERE operation_id='release-123'"
        ).fetchone()[0]
        self.assertEqual(count, 1)

    def test_restart_reconciles_unknown_response_without_retry(self):
        work = self.factory.admit(INTENT)
        self.factory.begin_operation(work.id, "release-456")
        self.factory.mark_indeterminate("release-456")
        self.factory.db.close()

        restarted = Factory(self.path)
        self.assertEqual(restarted.reconcile("release-456", "deployment-abc"), "COMPLETED")
        self.assertEqual(restarted.reconcile("release-456", "deployment-abc"), "COMPLETED")
        count = restarted.db.execute(
            "SELECT count(*) FROM operations WHERE operation_id='release-456'"
        ).fetchone()[0]
        self.assertEqual(count, 1)
        restarted.db.close()

    def test_material_decision_events_survive_restart(self):
        work = self.factory.admit(INTENT)
        self.factory.record_event(work.id, "authority_narrowed", {"reason": "outcome"})
        self.factory.db.close()
        restarted = Factory(self.path)
        self.assertEqual(restarted.events(work.id)[-1]["kind"], "authority_narrowed")
        restarted.db.close()


if __name__ == "__main__":
    unittest.main()
