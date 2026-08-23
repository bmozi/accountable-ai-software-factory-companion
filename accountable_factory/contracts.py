"""Canonical artifact contracts shared by schemas, examples, CLI, and factory.

© 2026 John Briggs — MIT licensed; see ../LICENSE-CODE.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any


DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")
KINDS = {"WorkOrder", "EvidenceRecord", "FactoryReceipt", "OutcomeObservation"}
REQUIRED: dict[str, tuple[str, ...]] = {
    "WorkOrder": (
        "id", "version", "workClass", "promise", "beneficiary", "owner",
        "consequenceOwner", "producerId", "releaseOwner", "learningOwner",
        "criteria", "prohibitions", "authority", "budgets", "evidenceFloor",
        "recovery", "outcome",
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


class ArtifactError(ValueError):
    """Raised when a reader artifact violates the canonical contract."""


def sha256_digest(content: bytes) -> str:
    return "sha256:" + hashlib.sha256(content).hexdigest()


def _nonempty_string(data: dict[str, Any], field: str, errors: list[str]) -> None:
    value = data.get(field)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{field} must be a non-empty string")


def _nonempty_list(data: dict[str, Any], field: str, errors: list[str]) -> None:
    value = data.get(field)
    if not isinstance(value, list) or not value:
        errors.append(f"{field} must be a non-empty list")


def validate_artifact(data: Any) -> list[str]:
    """Return every deterministic contract error found in one artifact."""

    errors: list[str] = []
    if not isinstance(data, dict):
        return ["root must be a JSON object"]
    if data.get("schemaVersion") != "1.0":
        errors.append("schemaVersion must be 1.0")

    kind = data.get("kind")
    if kind not in KINDS:
        return errors + [f"unknown kind: {kind!r}"]
    for field in REQUIRED[kind]:
        if field not in data:
            errors.append(f"missing required field: {field}")

    digest = data.get("candidateDigest")
    if digest is not None and (
        not isinstance(digest, str) or not DIGEST.fullmatch(digest)
    ):
        errors.append(
            "candidateDigest must be sha256 followed by 64 lowercase hex characters"
        )

    if kind == "WorkOrder":
        for field in (
            "id", "workClass", "promise", "beneficiary", "owner",
            "consequenceOwner", "producerId", "releaseOwner", "learningOwner",
        ):
            _nonempty_string(data, field, errors)
        for field in ("criteria", "prohibitions", "evidenceFloor"):
            _nonempty_list(data, field, errors)
        if not isinstance(data.get("version"), int) or data.get("version", 0) < 1:
            errors.append("version must be a positive integer")
        criteria = data.get("criteria", [])
        criterion_ids = {
            item.get("id") for item in criteria if isinstance(item, dict) and item.get("id")
        }
        if len(criterion_ids) != len(criteria):
            errors.append("criteria must have unique non-empty ids")
        floor = data.get("evidenceFloor", [])
        if any(item not in criterion_ids for item in floor):
            errors.append("evidenceFloor may name only declared criterion ids")
        authority = data.get("authority", {})
        budgets = data.get("budgets", {})
        recovery = data.get("recovery", {})
        outcome = data.get("outcome", {})
        if not isinstance(authority, dict) or not authority.get("environment"):
            errors.append("authority.environment must be explicit")
        if not isinstance(budgets, dict) or budgets.get("attempts", 0) < 1:
            errors.append("budgets.attempts must be at least 1")
        if isinstance(budgets, dict) and budgets.get("repairAttempts", -1) < 0:
            errors.append("budgets.repairAttempts must be zero or greater")
        if isinstance(budgets, dict) and budgets.get("costUnits", -1) < 0:
            errors.append("budgets.costUnits must be zero or greater")
        if not isinstance(recovery, dict) or recovery.get("lostResponse") != "reconcile-before-retry":
            errors.append("recovery.lostResponse must be reconcile-before-retry")
        if not isinstance(outcome, dict) or not outcome.get("countermetrics"):
            errors.append("outcome.countermetrics must be a non-empty list")

    elif kind == "EvidenceRecord":
        evaluator = data.get("evaluator", {})
        if not isinstance(evaluator, dict):
            errors.append("evaluator must be an object")
        elif data.get("decisive") and evaluator.get("actorId") == data.get("producerId"):
            errors.append("producer self-check cannot be decisive evidence")
        if data.get("result") not in {"pass", "fail", "inconclusive", "error"}:
            errors.append("result must be pass, fail, inconclusive, or error")
        _nonempty_string(data, "criterionId", errors)

    elif kind == "FactoryReceipt":
        _nonempty_list(data, "authorityUsed", errors)
        _nonempty_list(data, "evidenceRecordIds", errors)
        evidence_ids = data.get("evidenceRecordIds", [])
        authority_used = data.get("authorityUsed", [])
        if isinstance(authority_used, list) and any(
            not isinstance(item, str) or ":" not in item for item in authority_used
        ):
            errors.append("authorityUsed entries must be dimension:value")
        if isinstance(evidence_ids, list) and len(evidence_ids) != len(set(evidence_ids)):
            errors.append("evidenceRecordIds must be unique")
        operation = data.get("operation", {})
        if (
            isinstance(operation, dict)
            and operation.get("state") == "reconciled"
            and not operation.get("reconciliationEvidence")
        ):
            errors.append("reconciled operation requires reconciliationEvidence")
        disposition = data.get("disposition", {})
        if (
            isinstance(disposition, dict)
            and disposition.get("decision") == "exception"
            and not disposition.get("expiresAt")
        ):
            errors.append("exception disposition requires expiresAt")
        release = data.get("release", {})
        if not isinstance(release, dict) or release.get("mode") not in {
            "none", "advisory", "canary", "limited", "general"
        }:
            errors.append("invalid release mode")

    elif kind == "OutcomeObservation":
        _nonempty_list(data, "countermetrics", errors)
        if not isinstance(data.get("denominator"), int) or data.get("denominator", 0) < 1:
            errors.append("denominator must be a positive integer")
        if data.get("disposition") not in {
            "effective", "ineffective", "insufficient", "harmful", "not-yet-due"
        }:
            errors.append("invalid outcome disposition")

    return errors


def require_valid(data: Any) -> dict[str, Any]:
    errors = validate_artifact(data)
    if errors:
        raise ArtifactError("; ".join(errors))
    return data


def load_artifact(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ArtifactError(f"invalid JSON: {exc}") from exc
    return require_valid(data)
