# The Accountable AI Software Factory — Companion Repository

Reader-facing, runnable materials for *The Accountable AI Software Factory:
Building Governed, Verifiable Software at AI Speed* by John Briggs.

This repository turns the book's architecture into contracts, tests, and
operating instruments that readers can inspect, run, challenge, and adapt. The
book stands alone. The companion exists so readers do not have to retype the
reference implementation or reconstruct the decision artifacts from prose.

> **Series:** The Accountable AI Engineering Series — Book 3
> **Companion:** https://github.com/bmozi/accountable-ai-software-factory-companion

## Start with a failure, not a demo

```bash
git clone https://github.com/bmozi/accountable-ai-software-factory-companion.git
cd accountable-ai-software-factory-companion
./reference-factory/run-reader-journey.sh
```

The standard-library Python teaching core exercises incomplete intent, stale
state, producer self-approval, artifact-bound evidence, evaluator conflict,
duplicate operation identity, lost-response reconciliation, and durable
decision history. It uses SQLite and requires no model provider or API key.

Read [`START-HERE.md`](START-HERE.md) for a 30-minute path.

## What is here

| Path | Reader value |
|---|---|
| [`reference-factory/`](reference-factory/) | Vendor-neutral domain contracts, authority and evidence boundaries, recovery protocol, canonical fictional trace, twenty-four acceptance obligations, and runnable teaching code. |
| [`templates/`](templates/) | Factory charter, Work Order, risk-to-evidence, decision-rights, human-judgment, maturity, outcome, operations, threat-model, improvement, architecture-choice, and ninety-day pilot instruments. |
| [`MERLIN-PUBLIC-LESSONS.md`](MERLIN-PUBLIC-LESSONS.md) | Sanitized first-party failure lessons, evidence limits, and the responsibility-level architecture they changed. |
| [`PUBLIC-IMPLEMENTATIONS-TO-STUDY.md`](PUBLIC-IMPLEMENTATIONS-TO-STUDY.md) | A responsibility-by-responsibility map of public agent and software-factory projects. |
| [`EDITION-MAP.md`](EDITION-MAP.md) | Companion version relationship to Kindle and print editions. |
| [`ERRATA.md`](ERRATA.md) | Confirmed corrections and their disposition. |

## What this is—and is not

This is a small, executable teaching system. It demonstrates selected
accountability invariants; it is not a production starter kit, benchmark, or
claim of safety. Readers must select and operate their own identity, policy,
storage, execution, verification, source-control, delivery, and observability
systems.

The material derives from the book's vendor-neutral architecture and sanitized
lessons from Merlin Software Factory. It deliberately does not publish private
prompts, credentials, protected paths, exploitable control details, customer
information, or reconstructable production topology.

## The differentiating question

Public projects provide valuable pieces: specification workflows, coding-agent
runtimes, orchestration, durable execution, review stations, and fleet
management. This companion asks what must surround those pieces when the work
has organizational consequence:

- What versioned promise was admitted?
- Which identity held which authority?
- Which immutable artifact did each verdict evaluate?
- Who could disposition disagreement?
- What happened when a side effect may have occurred but its response was lost?
- Who owned the outcome after release?
- How could a proposed learning earn influence without changing its own judge?

## License

Executable Python and shell code under `reference-factory/example/` and
`reference-factory/run-reader-journey.sh` is MIT licensed. Written content,
templates, contracts, exercises, and explanatory material are CC BY-NC-SA 4.0.
See [`LICENSE`](LICENSE), [`LICENSE-CODE`](LICENSE-CODE), and
[`LICENSE-CONTENT`](LICENSE-CONTENT).

© 2026 John Briggs
