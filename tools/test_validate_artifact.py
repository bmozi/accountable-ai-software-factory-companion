"""Tests for the reader-facing artifact validator.

© 2026 John Briggs — MIT licensed; see ../LICENSE-CODE.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from validate_artifact import validate, validate_file


ROOT = Path(__file__).resolve().parents[1]


class ArtifactValidatorTests(unittest.TestCase):
    def test_published_valid_examples(self) -> None:
        for path in sorted((ROOT / "examples" / "artifacts").glob("*.valid.json")):
            with self.subTest(path=path.name):
                self.assertEqual(validate_file(path), [])

    def test_decisive_producer_self_approval_is_rejected(self) -> None:
        path = ROOT / "examples" / "artifacts" / "evidence.invalid-self-approval.json"
        errors = validate_file(path)
        self.assertIn("producer self-check cannot be decisive evidence", errors)

    def test_candidate_digest_is_artifact_bound(self) -> None:
        path = ROOT / "examples" / "artifacts" / "evidence.valid.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["candidateDigest"] = "candidate-latest"
        self.assertTrue(any("candidateDigest" in error for error in validate(data)))

    def test_exception_requires_expiry(self) -> None:
        path = ROOT / "examples" / "artifacts" / "factory-receipt.valid.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["disposition"]["decision"] = "exception"
        self.assertIn("exception disposition requires expiresAt", validate(data))

    def test_reconciled_operation_requires_evidence(self) -> None:
        path = ROOT / "examples" / "artifacts" / "factory-receipt.valid.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["operation"]["reconciliationEvidence"] = None
        self.assertIn(
            "reconciled operation requires reconciliationEvidence", validate(data)
        )


if __name__ == "__main__":
    unittest.main()
