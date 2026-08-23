#!/usr/bin/env python3
"""Validate companion JSON artifacts against the canonical contracts.

© 2026 John Briggs — MIT licensed; see ../LICENSE-CODE.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from accountable_factory.contracts import validate_artifact

validate = validate_artifact


def validate_file(path: Path) -> list[str]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"invalid JSON: {exc}"]
    return validate_artifact(data)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument("--expect-invalid", action="store_true")
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
