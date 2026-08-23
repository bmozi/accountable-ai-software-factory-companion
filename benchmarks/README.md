# Comparative pilot recorder

This directory deliberately ships a measurement harness, not flattering sample
results. Record observed runs from a pre-registered pilot and compare complete
operated outcomes—not model output volume.

```sh
python benchmarks/compare_pilot.py benchmarks/pilot-observations.example.json
```

Replace the example’s `null` values with measured data. The tool refuses to rank
incomplete arms, preserving denominator, cost, human effort, escaped defects,
and outcome evidence beside cycle time.
