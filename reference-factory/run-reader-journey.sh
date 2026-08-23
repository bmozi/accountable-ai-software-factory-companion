#!/bin/sh
# © 2026 John Briggs — MIT licensed; see ../LICENSE-CODE.
set -eu
cd "$(dirname "$0")/.."
PYTHONPATH=. python3 -m unittest discover -s reference-factory/example -p 'test_*.py' -v
PYTHONPATH=. python3 reference-factory/example/run_reader_journey.py
