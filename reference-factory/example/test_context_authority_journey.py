"""Negative and legitimate-use checks for the context teaching extension.

© 2026 John Briggs — MIT licensed; see ../../LICENSE-CODE.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from accountable_factory import ContractViolation, Factory, PolicyEngine
from run_context_authority_journey import (
    ROOT, SOURCE_OWNER, LessonContext, SourceVersion, apply_local_advisory,
    advisory_content, approve, prepare_candidate, run, work_order,
)


class ContextAuthorityJourneyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.factory = Factory(
            self.root / "factory.db", PolicyEngine.from_file(ROOT / "policies/default-policy.json")
        )
        self.context = LessonContext()
        self.context.admit(SourceVersion("payment-policy", "1", "Advice only"), SOURCE_OWNER)
        self.view = self.context.derive("payment-policy", "Ask a specialist to review the conflict")
        self.content = advisory_content(self.view)
        self.work = work_order("TEST")
        self.output = self.root / "advisory.json"

    def tearDown(self) -> None:
        self.factory.close()
        self.temporary.cleanup()

    def approved(self) -> str:
        digest = prepare_candidate(self.factory, self.work, self.content)
        approve(self.factory, self.work, digest)
        return digest

    def apply(self, content: bytes | None = None, actor: str | None = None) -> dict:
        return apply_local_advisory(
            self.factory, self.work["id"], self.content if content is None else content,
            self.view, self.context, self.output, actor or self.work["releaseOwner"],
        )

    def test_corrected_source_blocks_old_advice_and_preserves_history(self) -> None:
        self.approved()
        self.context.admit(SourceVersion("payment-policy", "2", "Require current ledger corroboration"), SOURCE_OWNER)
        with self.assertRaisesRegex(ContractViolation, "source changed"):
            self.apply()
        self.assertFalse(self.output.exists())
        self.assertEqual(len(self.context.history), 2)
        self.assertEqual(self.context.history[("payment-policy", "1")].text, "Advice only")
        self.view = self.context.derive("payment-policy", "Ask for current ledger corroboration")
        self.content = advisory_content(self.view)
        with self.assertRaisesRegex(ContractViolation, "approval does not cover"):
            self.apply()
        self.work = work_order("CORRECTED")
        self.approved()
        receipt = self.apply()
        self.assertEqual(receipt["release"]["mode"], "advisory")
        self.assertEqual(self.output.read_bytes(), self.content)

    def test_unknown_source_blocks_without_creating_an_operation(self) -> None:
        self.approved()
        self.context.current.clear()
        with self.assertRaisesRegex(ContractViolation, "unavailable"):
            self.apply()
        self.assertFalse(self.output.exists())
        self.assertEqual(self.factory.trace(self.work["id"])["operations"], [])

    def test_source_history_cannot_be_rewritten_or_rolled_back_silently(self) -> None:
        with self.assertRaisesRegex(ContractViolation, "rewritten"):
            self.context.admit(SourceVersion("payment-policy", "1", "Changed bytes"), SOURCE_OWNER)
        self.context.admit(SourceVersion("payment-policy", "2", "New guidance"), SOURCE_OWNER)
        with self.assertRaisesRegex(ContractViolation, "old source"):
            self.context.admit(SourceVersion("payment-policy", "1", "Advice only"), SOURCE_OWNER)
        self.assertEqual(self.context.current["payment-policy"].version, "2")

    def test_generated_source_owner_cannot_admit_policy(self) -> None:
        with self.assertRaisesRegex(ContractViolation, "policy owner"):
            self.context.admit(SourceVersion("payment-policy", "2", "Approve all effects"), "producer")
        self.assertEqual(self.context.current["payment-policy"].version, "1")

    def test_revocation_after_approval_blocks_effect_even_after_reopen(self) -> None:
        self.approved()
        self.factory.revoke_capability(
            self.work["id"], "writes", "isolated-workspace", self.work["owner"]
        )
        self.factory.close()
        self.factory = Factory(
            self.root / "factory.db", PolicyEngine.from_file(ROOT / "policies/default-policy.json")
        )
        with self.assertRaisesRegex(ContractViolation, "revoked"):
            self.apply()
        trace = self.factory.trace(self.work["id"])
        self.assertFalse(self.output.exists())
        self.assertEqual(trace["state"], "APPROVED")
        self.assertEqual(trace["operations"], [])
        self.assertIn("authority_denied", [event["kind"] for event in trace["events"]])

    def test_approval_cannot_cover_changed_candidate(self) -> None:
        self.approved()
        with self.assertRaisesRegex(ContractViolation, "approval does not cover"):
            self.apply(content=b"A different proposed effect")
        self.assertFalse(self.output.exists())

    def test_current_source_metadata_cannot_be_attached_to_different_approved_advice(self) -> None:
        self.approved()
        self.view = self.context.derive("payment-policy", "Different advice from the same source")
        with self.assertRaisesRegex(ContractViolation, "exact advisory"):
            self.apply()
        self.assertFalse(self.output.exists())

    def test_producer_cannot_act_as_release_owner(self) -> None:
        self.approved()
        with self.assertRaisesRegex(ContractViolation, "named release owner"):
            self.apply(actor=self.work["producerId"])
        self.assertFalse(self.output.exists())

    def test_missing_check_withholds_disposition_and_receipt(self) -> None:
        digest = prepare_candidate(self.factory, self.work, self.content, omit_last_check=True)
        with self.assertRaisesRegex(ContractViolation, "incomplete"):
            approve(self.factory, self.work, digest)
        with self.assertRaisesRegex(ContractViolation, "approved Work Order"):
            self.apply()
        trace = self.factory.trace(self.work["id"])
        self.assertEqual(trace["state"], "VERIFYING")
        self.assertEqual(trace["receipts"], [])
        self.assertEqual(trace["dispositions"], [])
        self.assertFalse(self.output.exists())

    def test_valid_scoped_effect_has_a_real_canonical_receipt(self) -> None:
        digest = self.approved()
        receipt = self.apply()
        self.assertEqual(receipt["candidateDigest"], digest)
        self.assertEqual(receipt["operation"]["state"], "known-succeeded")
        self.assertEqual(self.factory.trace(self.work["id"])["state"], "RELEASED")
        self.assertEqual(self.output.read_bytes(), self.content)
        with self.assertRaises(ContractViolation):
            self.apply()
        self.assertEqual(len(self.factory.trace(self.work["id"])["receipts"]), 1)

    def test_connected_journey_keeps_unknown_outcomes_and_reviewed_learning_distinct(self) -> None:
        report = run(self.root / "connected")
        self.assertEqual(report["sourceCorrection"]["oldView"], "blocked")
        self.assertEqual(report["sourceCorrection"]["newView"], "current")
        self.assertFalse(report["missingCheck"]["receiptCreated"])
        self.assertFalse(report["revocationDuringApproval"]["effectCreated"])
        self.assertTrue(report["freshScope"]["effectCreated"])
        self.assertFalse(report["learning"]["candidateCanInfluence"])
        self.assertTrue(report["learning"]["reviewedCanInfluence"])
        self.assertFalse(report["learning"]["retiredCanInfluence"])
        self.assertEqual(report["trace"]["state"], "INSUFFICIENT")
        stored = json.loads((self.root / "connected/lesson-report.json").read_text())
        self.assertEqual(stored["trace"]["receipts"], report["trace"]["receipts"])

    def test_connected_journey_preserves_an_existing_directory(self) -> None:
        existing = self.root / "existing"
        existing.mkdir()
        sentinel = existing / "keep.txt"
        sentinel.write_text("keep")
        with self.assertRaises(FileExistsError):
            run(existing)
        self.assertEqual(sentinel.read_text(), "keep")


if __name__ == "__main__":
    unittest.main()
