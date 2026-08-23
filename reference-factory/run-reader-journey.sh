#!/bin/sh
set -eu
cd "$(dirname "$0")/example"
python3 -m unittest -v test_reference_factory.py
python3 run_reader_journey.py
