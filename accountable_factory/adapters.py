"""Local, dependency-free adapters for the complete reader journey.

© 2026 John Briggs — MIT licensed; see ../LICENSE-CODE.
"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Any


class LostResponse(RuntimeError):
    """The effect may have happened, but its response was not received."""


class DeterministicProducer:
    """A provider-neutral stand-in that makes the orchestration testable offline."""

    def __init__(self, name: str):
        self.name = name

    def produce(self, work_order: dict[str, Any]) -> bytes:
        return (
            json.dumps(
                {
                    "provider": self.name,
                    "workOrderId": work_order["id"],
                    "promise": work_order["promise"],
                    "mode": work_order["authority"]["mode"],
                },
                indent=2,
                sort_keys=True,
            )
            + "\n"
        ).encode()


class LocalGitAdapter:
    """Create one local Git effect and reconcile it by semantic operation id."""

    def __init__(self, repository: str | Path):
        self.repository = Path(repository)
        self.repository.mkdir(parents=True, exist_ok=True)
        if not (self.repository / ".git").exists():
            self._run("git", "init", "-q")
            self._run("git", "config", "user.name", "Factory Reader")
            self._run("git", "config", "user.email", "reader@example.invalid")

    def publish(
        self, operation_id: str, candidate: bytes, *, lose_response: bool = False
    ) -> str:
        tag = self._tag(operation_id)
        existing = self.observe(operation_id)
        if existing:
            return existing
        (self.repository / "candidate.json").write_bytes(candidate)
        self._run("git", "add", "candidate.json")
        self._run("git", "commit", "-q", "-m", f"Apply {operation_id}")
        effect_ref = self._run("git", "rev-parse", "HEAD").strip()
        self._run("git", "tag", tag, effect_ref)
        if lose_response:
            raise LostResponse(operation_id)
        return effect_ref

    def observe(self, operation_id: str) -> str | None:
        tag = self._tag(operation_id)
        result = subprocess.run(
            ["git", "rev-parse", "-q", "--verify", f"refs/tags/{tag}"],
            cwd=self.repository,
            text=True,
            capture_output=True,
            check=False,
        )
        return result.stdout.strip() or None

    def effect_count(self, operation_id: str) -> int:
        return 1 if self.observe(operation_id) else 0

    def _tag(self, operation_id: str) -> str:
        safe = re.sub(r"[^A-Za-z0-9._-]", "-", operation_id)
        return f"factory-operation-{safe}"

    def _run(self, *args: str) -> str:
        return subprocess.run(
            list(args), cwd=self.repository, text=True, capture_output=True,
            check=True,
        ).stdout
