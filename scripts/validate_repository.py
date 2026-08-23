#!/usr/bin/env python3
"""Validate the public companion's published paths and local Markdown links."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.3.1"
PUBLISHED_PATHS = (
    "companion/factory-charter-template.md",
    "companion/memory-governance-workbook.md",
    "companion/provider-tenant-capacity-design.md",
    "companion/risk-to-evidence-matrix.md",
    "companion/comparative-pilot-protocol.md",
    "companion/continuous-improvement-experiment.md",
    "companion/ninety-day-pilot-workbook.md",
)
LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
EXECUTABLE_SOURCES = (
    "reference-factory/example/reference_factory.py",
    "reference-factory/example/run_reader_journey.py",
    "reference-factory/example/test_reference_factory.py",
    "reference-factory/run-reader-journey.sh",
)
REQUIRED_PUBLIC_FILES = (
    "COMMERCIAL-USE.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "LICENSE",
    "LICENSE-CODE",
    "LICENSE-CONTENT",
    ".github/ISSUE_TEMPLATE/errata.yml",
    ".github/ISSUE_TEMPLATE/broken-resource.yml",
    ".github/ISSUE_TEMPLATE/config.yml",
)


def local_target(source: Path, raw_target: str) -> Path | None:
    target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
    if not target or target.startswith(("#", "http://", "https://", "mailto:")):
        return None
    target = unquote(target.split("#", 1)[0])
    return (source.parent / target).resolve()


def main() -> int:
    errors: list[str] = []

    for relative in (*PUBLISHED_PATHS, *REQUIRED_PUBLIC_FILES):
        if not (ROOT / relative).is_file():
            errors.append(f"missing required public path: {relative}")

    for source in ROOT.rglob("*.md"):
        if ".git" in source.parts:
            continue
        for raw_target in LINK.findall(source.read_text(encoding="utf-8")):
            target = local_target(source, raw_target)
            if target is not None and not target.exists():
                errors.append(
                    f"broken local link: {source.relative_to(ROOT)} -> {raw_target}"
                )

    for relative in EXECUTABLE_SOURCES:
        source = ROOT / relative
        if source.is_file() and "MIT licensed" not in "\n".join(
            source.read_text(encoding="utf-8").splitlines()[:16]
        ):
            errors.append(f"executable source lacks traveling MIT notice: {relative}")

    citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    edition_map = (ROOT / "EDITION-MAP.md").read_text(encoding="utf-8")
    if f"version: {VERSION}" not in citation:
        errors.append(f"CITATION.cff does not name current version {VERSION}")
    if f"## {VERSION} " not in changelog:
        errors.append(f"CHANGELOG.md does not name current version {VERSION}")
    if f"| {VERSION} |" not in edition_map:
        errors.append(f"EDITION-MAP.md does not name current version {VERSION}")

    for source in (ROOT / "templates").glob("*.md"):
        text = source.read_text(encoding="utf-8").lower()
        for first, second in (("working", "draft"), ("to", "do"), ("fix", "me")):
            phrase = f"{first} {second}"
            if phrase in text:
                errors.append(
                    f"reader-facing production language in {source.relative_to(ROOT)}: {phrase}"
                )

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    print(
        f"Validated companion {VERSION}: {len(PUBLISHED_PATHS)} published paths, "
        "public governance files, license notices, version pins, and all local links."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
