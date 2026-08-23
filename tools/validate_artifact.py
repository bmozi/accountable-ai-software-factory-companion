#!/usr/bin/env python3
"""Validate selected accountability invariants in companion JSON artifacts.

© 2026 John Briggs — MIT licensed; see ../LICENSE-CODE.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")
REQUIRED: dict[str, tuple[str, ...]] = {
    "WorkOrder": (
        "id", "version", "promise", "beneficiary", "owner",
        "consequenceOwner", "producerId", "criteria", "prohibitions",
        "authority", "budgets", "evidenceFloor", "recovery", "outcome",
    ),
    "EvidenceRecord": (
        "id", "workOrderId", "candidateDigest", "criterionId", "producerId",
        "evaluator", "method", "result", "decisive", "observedAt", "limitations",
    ),
    "FactoryReceipt": (
        "id", "workOrderId", "intentVersion", "candidateDigest",
        "authorityUsed", "evidenceRecordIds", "disposition", "operation",
        "release", "recoveryOwner", "createdAt",
    ),
    "OutcomeObservation": (
        "id", "receiptId", "observedAt", "window", "primaryMeasure",
        "countermetrics", "denominator", "limitations", "disposition",
        "decisionOwner",
    ),
}


def require_nonempty_list(data: dict[str, Any], field: str, errors: list[str]) -> None:
    value = data.get(field)
    if not isinstance(value, list) or not value:
        errors.append(f"{field} must be a non-empty list")


def validate(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["root must be a JSON object"]
    if data.get("schemaVersion") != "1.0":
        errors.append("schemaVersion must be 1.0")

    kind = data.get("kind")
    if kind not in REQUIRED:
        return errors + [f"unknown kind: {kind!r}"]
    for field in REQUIRED[kind]:
        if field not in data:
            errors.append(f"missing required field: {field}")

    digest = data.get("candidateDigest")
    if digest is not None and (not isinstance(digest, str) or not DIGEST.fullmatch(digest)):
        errors.append("candidateDigest must be sha256 followed by 64 lowercase hex characters")

    if kind == "WorkOrder":
        for field in ("criteria", "prohibitions", "evidenceFloor"):
            require_nonempty_list(data, field, errors)
        authority = data.get("authority", {})
        budgets = data.get("budgets", {})
        recovery = data.get("recovery", {})
        if not isinstance(authority, dict) or not authority.get("environment"):
            errors.append("authority.environment must be explicit")
        if not isinstance(budgets, dict) or budgets.get("attempts", 0) < 1:
            errors.append("budgets.attempts must be at least 1")
        if not isinstance(recovery, dict) or recovery.get("lostResponse") != "reconcile-before-retry":
            errors.append("recovery.lostResponse must be reconcile-before-retry")

    elif kind == "EvidenceRecord":
        evaluator = data.get("evaluator", {})
        if not isinstance(evaluator, dict):
            errors.append("evaluator must be an object")
        elif data.get("decisive") and evaluator.get("actorId") == data.get("producerId"):
            errors.append("producer self-check cannot be decisive evidence")
        if data.get("result") not in {"pass", "fail", "inconclusive", "error"}:
            errors.append("result must be pass, fail, inconclusive, or error")

    elif kind == "FactoryReceipt":
        require_nonempty_list(data, "authorityUsed", errors)
        require_nonempty_list(data, "evidenceRecordIds", errors)
        evidence_ids = data.get("evidenceRecordIds", [])
        if isinstance(evidence_ids, list) and len(evidence_ids) != len(set(evidence_ids)):
            errors.append("evidenceRecordIds must be unique")
        operation = data.get("operation", {})
        if isinstance(operation, dict) and operation.get("state") == "reconciled" and not operation.get("reconciliationEvidence"):
            errors.append("reconciled operation requires reconciliationEvidence")
        disposition = data.get("disposition", {})
        if isinstance(disposition, dict) and disposition.get("decision") == "exception" and not disposition.get("expiresAt"):
            errors.append("exception disposition requires expiresAt")

    elif kind == "OutcomeObservation":
        require_nonempty_list(data, "countermetrics", errors)
        if not isinstance(data.get("denominator"), int) or data.get("denominator", 0) < 1:
            errors.append("denominator must be a positive integer")
        if data.get("disposition") not in {
            "effective", "ineffective", "insufficient", "harmful", "not-yet-due"
        }:
            errors.append("invalid outcome disposition")

    return errors


def validate_file(path: Path) -> list[str]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"invalid JSON: {exc}"]
    return validate(data)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument(
        "--expect-invalid",
        action="store_true",
        help="Succeed only when every supplied artifact is rejected.",
    )
    args = parser.parse_args()
    failed = False
    for path in args.files:
        errors = validate_file(path)
        if args.expect_invalid:
            if errors:
                print(f"EXPECTED REJECTION {path}: {'; '.join(errors)}")
            else:
                print(f"UNEXPECTED ACCEPTANCE {path}", file=sys.stderr)
                failed = True
        elif errors:
            print(f"INVALID {path}: {'; '.join(errors)}", file=sys.stderr)
            failed = True
        else:
            print(f"VALID {path}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
