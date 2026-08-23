#!/usr/bin/env python3
"""Validate the public companion's published paths and local Markdown links."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
PUBLISHED_PATHS = (
    "companion/factory-charter-template.md",
    "companion/memory-governance-workbook.md",
    "companion/provider-tenant-capacity-design.md",
    "companion/risk-to-evidence-matrix.md",
    "companion/comparative-pilot-protocol.md",
    "companion/continuous-improvement-experiment.md",
    "companion/ninety-day-pilot-workbook.md",
)
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")


def local_target(source: Path, raw_target: str) -> Path | None:
    target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
    if not target or target.startswith(("#", "http://", "https://", "mailto:")):
        return None
    target = unquote(target.split("#", 1)[0])
    return (source.parent / target).resolve()


def main() -> int:
    errors: list[str] = []

    for relative in PUBLISHED_PATHS:
        if not (ROOT / relative).is_file():
            errors.append(f"missing published Book 3 path: {relative}")

    for source in ROOT.rglob("*.md"):
        if ".git" in source.parts:
            continue
        for raw_target in LINK.findall(source.read_text(encoding="utf-8")):
            target = local_target(source, raw_target)
            if target is not None and not target.exists():
                errors.append(
                    f"broken local link: {source.relative_to(ROOT)} -> {raw_target}"
                )

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    print(
        f"Validated {len(PUBLISHED_PATHS)} published paths and all local Markdown links."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
