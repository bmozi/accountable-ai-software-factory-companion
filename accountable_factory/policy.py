"""Deterministic admission and authority policy for the teaching factory.

© 2026 John Briggs — MIT licensed; see ../LICENSE-CODE.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class PolicyViolation(ValueError):
    pass


class PolicyEngine:
    def __init__(self, document: dict[str, Any]):
        self.document = document

    @classmethod
    def from_file(cls, path: str | Path) -> "PolicyEngine":
        return cls(json.loads(Path(path).read_text(encoding="utf-8")))

    def evaluate_work_order(self, work_order: dict[str, Any]) -> list[str]:
        errors: list[str] = []
        work_class = work_order.get("workClass")
        rule = self.document.get("workClasses", {}).get(work_class)
        if not isinstance(rule, dict):
            return [f"work class is not admitted by policy: {work_class}"]

        authority = work_order.get("authority", {})
        if authority.get("mode") not in rule.get("allowedModes", []):
            errors.append(f"authority mode is not allowed: {authority.get('mode')}")
        if authority.get("environment") not in rule.get("allowedEnvironments", []):
            errors.append(
                f"environment is not allowed: {authority.get('environment')}"
            )
        if authority.get("delegation", 0) > rule.get("maxDelegation", 0):
            errors.append("delegation exceeds policy maximum")
        if work_order.get("budgets", {}).get("costUnits", 0) > rule.get("maxCostUnits", 0):
            errors.append("cost budget exceeds policy maximum")
        missing = sorted(
            set(rule.get("requiredProhibitions", []))
            - set(work_order.get("prohibitions", []))
        )
        if missing:
            errors.append(f"required prohibitions missing: {', '.join(missing)}")
        return errors

    def assert_authority(
        self, work_order: dict[str, Any], dimension: str, value: str
    ) -> None:
        authority = work_order.get("authority", {})
        allowed = authority.get(dimension)
        if isinstance(allowed, list) and value in allowed:
            return
        if isinstance(allowed, str) and value == allowed:
            return
        raise PolicyViolation(f"authority denied: {dimension}={value}")
