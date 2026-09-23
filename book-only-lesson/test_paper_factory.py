"""Run: python3 -m unittest -v test_paper_factory.py"""
import tempfile
import unittest
from paper_factory import Factory


class BoundaryTests(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.f = Factory(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)
        self.addCleanup(lambda: self.f.close())

    def version(self):
        return self.f.read()["version"]

    def ready(self, mode="half_up"):
        self.f.admit(0, "owner", "round cents, sandbox only")
        self.f.attempt(1, "producer")
        self.f.candidate(2, "producer", mode)
        self.f.evaluate(3, "evaluator",
                        self.f.read()["candidate"]["digest"])

    def prepared(self):
        self.ready()
        self.f.decide(4, "reviewer", "approve", "bounded trial")
        self.f.prepare(5, "releaser", "OP-1")

    def blocked(self, message, action):
        before = self.f.read()
        with self.assertRaisesRegex(ValueError, message):
            action()
        self.assertEqual(before, self.f.read())

    def test_admission_and_stale_writer(self):
        self.blocked("ineligible", lambda:
                     self.f.admit(0, "owner", "make it safe"))
        self.f.admit(0, "owner", "round cents, sandbox only")
        self.blocked("stale", lambda: self.f.attempt(0, "producer"))

    def test_producer_and_wrong_digest_cannot_supply_evidence(self):
        self.f.admit(0, "owner", "round cents, sandbox only")
        self.f.attempt(1, "producer")
        self.f.candidate(2, "producer", "half_up")
        d = self.f.read()["candidate"]["digest"]
        self.blocked("evaluator", lambda:
                     self.f.evaluate(3, "producer", d))
        self.blocked("wrong candidate", lambda:
                     self.f.evaluate(3, "evaluator", "old digest"))

    def test_failed_fixture_blocks_approval(self):
        self.ready("half_even")
        self.assertEqual("1.00", self.f.read()["verdict"]["actual"])
        self.blocked("blocking", lambda:
                     self.f.decide(4, "reviewer", "approve", "hope"))
        self.f.decide(4, "reviewer", "reject", "rounding wrong")
        self.blocked("not approved", lambda:
                     self.f.prepare(5, "releaser", "OP-1"))

    def test_release_requires_disposition_and_current_grant(self):
        self.ready()
        self.blocked("not approved", lambda:
                     self.f.prepare(4, "releaser", "OP-1"))
        self.f.decide(4, "reviewer", "approve", "bounded pilot")
        self.f.prepare(5, "releaser", "OP-1")
        self.f.revoke(6, "owner")
        self.blocked("revoked", lambda: self.f.send(7, "releaser"))
        self.assertEqual(0, self.f.target.execute(
            "SELECT count(*) FROM effects").fetchone()[0])

    def test_lost_reply_restart_and_key_binding(self):
        self.prepared()
        with self.assertRaises(TimeoutError):
            self.f.send(6, "releaser", lose_reply=True)
        self.assertEqual("indeterminate", self.f.read()["stage"])
        self.f.close()
        self.f = Factory(self.tmp.name)
        effect = self.f.read()["effect"]
        self.f.target_apply(effect)  # Same key and arguments: no copy.
        changed = dict(effect, digest="different artifact")
        with self.assertRaisesRegex(ValueError, "key conflict"):
            self.f.target_apply(changed)
        self.f.revoke(6, "owner")
        self.f.reconcile(7, "operator")  # Read despite revoked release.
        self.assertEqual("target query",
                         self.f.read()["receipt"]["via"])
        self.assertEqual(1, self.f.target.execute(
            "SELECT count(*) FROM effects").fetchone()[0])
        self.blocked("no intent", lambda: self.f.send(8, "releaser"))

    def test_revision_invalidates_evidence_and_decision(self):
        self.ready()
        old_digest = self.f.read()["candidate"]["digest"]
        self.f.decide(4, "reviewer", "approve", "bounded trial")
        self.f.revise(5, "reviewer", "compare alternative rounding")
        self.assertNotIn("decision", self.f.read())
        self.assertNotIn("verdict", self.f.read())
        self.f.attempt(6, "producer")
        self.f.candidate(7, "producer", "half_even")
        self.blocked("wrong candidate", lambda:
                     self.f.evaluate(8, "evaluator", old_digest))
        new_digest = self.f.read()["candidate"]["digest"]
        self.f.evaluate(8, "evaluator", new_digest)
        self.f.revise(9, "reviewer", "restore required rule")
        self.f.attempt(10, "producer")
        self.f.candidate(11, "producer", "half_up")
        self.f.evaluate(12, "evaluator", old_digest)
        self.f.decide(13, "reviewer", "approve", "fresh fixture passed")
        self.assertEqual(13,
                         self.f.read()["decision"]["evidence_version"])
        self.assertEqual(14, self.f.db.execute(
            "SELECT count(*) FROM history").fetchone()[0])

    def test_attempt_budget_and_wrong_role_approval(self):
        self.ready()
        self.blocked("reviewer", lambda:
                     self.f.decide(4, "producer", "approve", "my work"))
        for index in range(2):
            v = self.version()
            self.f.revise(v, "reviewer", "recheck")
            self.f.attempt(v + 1, "producer")
            self.f.candidate(v + 2, "producer", "half_up")
            d = self.f.read()["candidate"]["digest"]
            self.f.evaluate(v + 3, "evaluator", d)
        self.f.revise(self.version(), "reviewer", "one more")
        self.blocked("budget exhausted", lambda:
                     self.f.attempt(self.version(), "producer"))
        self.assertEqual(3, self.f.read()["attempts"])

    def test_no_target_receipt_does_not_fabricate_completion(self):
        self.prepared()
        self.blocked("retain uncertainty", lambda:
                     self.f.reconcile(6, "operator"))
        self.assertEqual("indeterminate", self.f.read()["stage"])

    def test_harm_is_not_hidden_by_small_sample(self):
        self.prepared()
        self.f.send(6, "releaser")
        self.f.observe(7, "outcome-owner", 8, 1)
        self.assertEqual("harmful", self.f.read()["outcome"]["result"])
        self.f.propose(8, "analyst", "investigate with wider fixtures")
        self.assertEqual("none", self.f.read()["learning"]["authority"])
        self.assertEqual("teaching-1", self.f.read()["work"]["policy"])

    def test_short_clean_observation_is_insufficient(self):
        self.prepared()
        self.f.send(6, "releaser")
        self.f.observe(7, "outcome-owner", 8, 0)
        self.assertEqual("insufficient",
                         self.f.read()["outcome"]["result"])
        rows = self.f.db.execute(
            "SELECT count(*) FROM history").fetchone()[0]
        self.assertEqual(self.version(), rows)



if __name__ == "__main__":
    unittest.main()
