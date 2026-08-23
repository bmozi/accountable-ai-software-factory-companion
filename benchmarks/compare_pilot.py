#!/usr/bin/env python3
"""Render measured comparative-pilot observations without inventing results.

© 2026 John Briggs — MIT licensed; see ../LICENSE-CODE.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


FIELDS = ("completedWorkOrders", "medianCycleMinutes", "humanMinutes", "costUnits", "escapedDefects", "outcomeSuccesses")


def main() -> int:
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    arms = data.get("arms", [])
    missing = [f"{arm.get('name')}:{field}" for arm in arms for field in FIELDS if arm.get(field) is None]
    if len(arms) < 2 or missing:
        print("INCOMPLETE: no ranking produced; missing " + ", ".join(missing), file=sys.stderr); return 2
    print("| Arm | Completed | Cycle min | Human min | Cost units | Escaped defects | Outcome success rate |")
    print("|---|---:|---:|---:|---:|---:|---:|")
    for arm in arms:
        rate = arm["outcomeSuccesses"] / arm["completedWorkOrders"] if arm["completedWorkOrders"] else 0
        print(f"| {arm['name']} | {arm['completedWorkOrders']} | {arm['medianCycleMinutes']} | {arm['humanMinutes']} | {arm['costUnits']} | {arm['escapedDefects']} | {rate:.1%} |")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
