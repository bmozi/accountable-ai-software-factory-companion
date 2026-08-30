#!/usr/bin/env python3
"""Validate the public companion's publication and curriculum contracts.

© 2026 John Briggs — MIT licensed; see ../LICENSE-CODE.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
VERSION = "1.2.1"
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
    "accountable_factory/__init__.py",
    "accountable_factory/adapters.py",
    "accountable_factory/cli.py",
    "accountable_factory/contracts.py",
    "accountable_factory/factory.py",
    "accountable_factory/policy.py",
    "benchmarks/compare_pilot.py",
    "reference-factory/example/reference_factory.py",
    "reference-factory/example/run_reader_journey.py",
    "reference-factory/example/test_reference_factory.py",
    "reference-factory/run-reader-journey.sh",
    "scripts/build_reader_bundle.py",
    "scripts/validate_repository.py",
    "tools/validate_artifact.py",
    "tools/test_validate_artifact.py",
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
    ".github/ISSUE_TEMPLATE/reader-usability.yml",
    ".github/ISSUE_TEMPLATE/config.yml",
    "READER-USABILITY-PASS.md",
)
PREMIUM_PATHS = (
    "FROM-GOVERNED-LOOP-TO-FACTORY.md",
    "INDEX.md",
    "SERIES-PROGRESSION.md",
    "assessment/accountable-factory-diagnostic.md",
    "benchmarks/pilot-observations.example.json",
    "decisions/architecture-decision-starters.md",
    "diagrams/accountable-factory-visual-guide.md",
    "examples/meridian-ledger-complete-trace.md",
    "exercises/failure-laboratory.md",
    "implementation/minimum-viable-accountable-factory.md",
    "integrations/github-actions/accountability-gates.yml",
    "learning-paths/README.md",
    "leadership/ai-native-build-versus-buy-calculator.md",
    "leadership/enterprise-agent-role-and-decision-rights-map.md",
    "merlin/sanitized-pattern-cards.md",
    "policies/default-policy.json",
    "reference-factory/Dockerfile",
    "release-assets/README.md",
    "schemas/work-order.schema.json",
    "schemas/evidence-record.schema.json",
    "schemas/factory-receipt.schema.json",
    "schemas/outcome-observation.schema.json",
    "study-guides/chapter-workbook.md",
    "study-guides/chapters/README.md",
    "templates/factory-balance-sheet.md",
    "tools/validate_artifact.py",
    "tools/test_validate_artifact.py",
    "workforce/ai-practice-and-guardrail-guide.md",
)


def local_target(source: Path, raw_target: str) -> Path | None:
    target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
    if not target or target.startswith(("#", "http://", "https://", "mailto:")):
        return None
    target = unquote(target.split("#", 1)[0])
    return (source.parent / target).resolve()


def main() -> int:
    errors: list[str] = []

    for relative in (*PUBLISHED_PATHS, *REQUIRED_PUBLIC_FILES, *PREMIUM_PATHS):
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

    for source in ROOT.rglob("*.json"):
        if ".git" in source.parts or "dist" in source.parts:
            continue
        try:
            json.loads(source.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            errors.append(f"invalid JSON: {source.relative_to(ROOT)}: {exc}")

    promised_counts = (
        ("study-guides/chapter-workbook.md", "## Chapter ", 18, "chapters"),
        ("exercises/failure-laboratory.md", "## Drill ", 12, "failure drills"),
        ("diagrams/accountable-factory-visual-guide.md", "```mermaid", 5, "diagrams"),
        ("merlin/sanitized-pattern-cards.md", "## Card ", 9, "Merlin pattern cards"),
    )
    for relative, marker, expected, label in promised_counts:
        actual = (ROOT / relative).read_text(encoding="utf-8").count(marker)
        if actual != expected:
            errors.append(f"{relative} contains {actual} {label}; expected {expected}")

    template_count = len(list((ROOT / "templates").glob("*.md")))
    if template_count != 19:
        errors.append(f"templates contains {template_count} instruments; expected 19")
    chapter_guide_count = len(
        list((ROOT / "study-guides" / "chapters").glob("learning-guide-ch*.md"))
    )
    if chapter_guide_count != 18:
        errors.append(
            f"study-guides/chapters contains {chapter_guide_count} guides; expected 18"
        )
    schema_count = len(list((ROOT / "schemas").glob("*.schema.json")))
    if schema_count != 4:
        errors.append(f"schemas contains {schema_count} contracts; expected 4")
    valid_example_count = len(list((ROOT / "examples" / "artifacts").glob("*.valid.json")))
    if valid_example_count != 4:
        errors.append(
            f"examples/artifacts contains {valid_example_count} valid records; expected 4"
        )

    acceptance_source = (ROOT / "reference-factory/example/test_reference_factory.py").read_text(encoding="utf-8")
    acceptance_ids = re.findall(r"def test_(a\d{2})_", acceptance_source)
    expected_ids = [f"a{number:02d}" for number in range(1, 25)]
    if acceptance_ids != expected_ids:
        errors.append(f"executable acceptance coverage is {acceptance_ids}; expected {expected_ids}")

    canonical_import = (ROOT / "tools/validate_artifact.py").read_text(encoding="utf-8")
    if "from accountable_factory.contracts import validate_artifact" not in canonical_import:
        errors.append("artifact validator does not consume the canonical contract")

    compatibility_source = (ROOT / "reference-factory/example/reference_factory.py").read_text(encoding="utf-8")
    if "class Factory" in compatibility_source or "intent_json" in compatibility_source:
        errors.append("retired split factory model returned under reference-factory/example")
    work_order_schema = (ROOT / "schemas/work-order.schema.json").read_text(encoding="utf-8")
    for canonical_role in ("workClass", "releaseOwner", "learningOwner"):
        if canonical_role not in work_order_schema:
            errors.append(f"Work Order schema lacks canonical role: {canonical_role}")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    print(
        f"Validated companion laboratory {VERSION}: {len(PUBLISHED_PATHS)} published "
        f"paths, {len(PREMIUM_PATHS)} curriculum contracts, public governance, "
        "licenses, versions, JSON, and all local links."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
