#!/usr/bin/env python3
"""Build a deterministic, versioned reader bundle for a companion release.

© 2026 John Briggs — MIT licensed; see ../LICENSE-CODE.
"""

from __future__ import annotations

import hashlib
import json
import re
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
VERSION_PATTERN = re.compile(r"^version:\s*([0-9]+\.[0-9]+\.[0-9]+)\s*$", re.MULTILINE)
TOP_LEVEL = (
    "BOOK-TO-COMPANION-MAP.md",
    "CHANGELOG.md",
    "CITATION.cff",
    "COMMERCIAL-USE.md",
    "CONTRIBUTING.md",
    "EDITION-MAP.md",
    "ERRATA.md",
    "INDEX.md",
    "LICENSE",
    "LICENSE-CODE",
    "LICENSE-CONTENT",
    "MERLIN-PUBLIC-LESSONS.md",
    "PUBLIC-IMPLEMENTATIONS-TO-STUDY.md",
    "README.md",
    "SECURITY.md",
    "START-HERE.md",
)
DIRECTORIES = (
    "assessment",
    "companion",
    "decisions",
    "diagrams",
    "examples",
    "exercises",
    "implementation",
    "learning-paths",
    "leadership",
    "merlin",
    "reference-factory",
    "release-assets",
    "schemas",
    "study-guides",
    "templates",
    "tools",
    "workforce",
)
EXCLUDED_SUFFIXES = {".db", ".pyc"}


def current_version() -> str:
    match = VERSION_PATTERN.search((ROOT / "CITATION.cff").read_text(encoding="utf-8"))
    if not match:
        raise RuntimeError("CITATION.cff does not contain a semantic version")
    return match.group(1)


def included_files() -> list[Path]:
    files = [ROOT / name for name in TOP_LEVEL]
    for directory in DIRECTORIES:
        files.extend(path for path in (ROOT / directory).rglob("*") if path.is_file())
    return sorted(
        path
        for path in set(files)
        if path.suffix not in EXCLUDED_SUFFIXES
        and "__pycache__" not in path.parts
        and not path.name.startswith(".DS_Store")
    )


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_zip(path: Path, prefix: str, files: list[Path], manifest: bytes) -> None:
    timestamp = (2026, 8, 22, 0, 0, 0)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for source in files:
            relative = source.relative_to(ROOT).as_posix()
            info = zipfile.ZipInfo(f"{prefix}/{relative}", timestamp)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, source.read_bytes())
        info = zipfile.ZipInfo(f"{prefix}/BUNDLE-MANIFEST.json", timestamp)
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o100644 << 16
        archive.writestr(info, manifest)


def main() -> int:
    version = current_version()
    prefix = f"accountable-ai-software-factory-companion-v{version}"
    files = included_files()
    missing = [str(path.relative_to(ROOT)) for path in files if not path.is_file()]
    if missing:
        raise RuntimeError(f"missing bundle inputs: {missing}")

    manifest_data = {
        "title": "The Accountable AI Software Factory Companion",
        "version": version,
        "bookEdition": "first edition",
        "fileCount": len(files),
        "files": [
            {"path": path.relative_to(ROOT).as_posix(), "sha256": digest(path)}
            for path in files
        ],
    }
    manifest = (json.dumps(manifest_data, indent=2, sort_keys=True) + "\n").encode()

    DIST.mkdir(exist_ok=True)
    archive_path = DIST / f"{prefix}.zip"
    manifest_path = DIST / f"{prefix}-manifest.json"
    checksums_path = DIST / "SHA256SUMS.txt"
    write_zip(archive_path, prefix, files, manifest)
    manifest_path.write_bytes(manifest)
    checksums_path.write_text(
        f"{digest(archive_path)}  {archive_path.name}\n"
        f"{digest(manifest_path)}  {manifest_path.name}\n",
        encoding="utf-8",
    )
    print(f"Built {archive_path.name} with {len(files)} reader files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
