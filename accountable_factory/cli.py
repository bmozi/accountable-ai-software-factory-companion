#!/usr/bin/env python3
"""Command-line entry points for validation, inspection, and the reader journey.

© 2026 John Briggs — MIT licensed; see ../LICENSE-CODE.
"""

from __future__ import annotations

import argparse
import json
import runpy
from pathlib import Path

from .contracts import load_artifact
from .factory import Factory
from .policy import PolicyEngine


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(prog="accountable-factory")
    sub = parser.add_subparsers(dest="command", required=True)
    validate = sub.add_parser("validate", help="Validate a canonical JSON artifact")
    validate.add_argument("artifact", type=Path)
    inspect = sub.add_parser("inspect", help="Print a durable Work Order trace")
    inspect.add_argument("database", type=Path); inspect.add_argument("work_order")
    inspect.add_argument("--policy", type=Path, default=ROOT / "policies/default-policy.json")
    sub.add_parser("journey", help="Run the complete offline reader journey")
    args = parser.parse_args()
    if args.command == "validate":
        print(json.dumps(load_artifact(args.artifact), indent=2, sort_keys=True)); return 0
    if args.command == "journey":
        runpy.run_path(str(ROOT / "reference-factory/example/run_reader_journey.py"), run_name="__main__"); return 0
    factory = Factory(args.database, PolicyEngine.from_file(args.policy))
    try:
        print(json.dumps(factory.trace(args.work_order), indent=2, sort_keys=True))
    finally:
        factory.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
