# The Accountable AI Software Factory — Companion Repository

Reader-facing, runnable materials for *The Accountable AI Software Factory:
Building Governed, Verifiable Software at AI Speed* by John Briggs.

This repository turns the book's architecture into contracts, tests, and
operating instruments that readers can inspect, run, challenge, and adapt. The
book is the curriculum; this repository is its laboratory. The companion
exists so readers do not have to retype the reference implementation or
reconstruct the decision artifacts from prose. It does not reproduce the
book's reasoning, narrative consequences, architectural tradeoffs, or guidance
for deciding when authority has been earned.

> **Series:** The Accountable AI Engineering Series — Book 3
> **Companion:** https://github.com/bmozi/accountable-ai-software-factory-companion

This volume builds on the public
[*Harnessing the Horse* companion](https://github.com/bmozi/harnessing-the-horse-companion).
Book 2 teaches disciplined AI-assisted work; this repository carries that
discipline into an accountable production system.

## Start with a failure, not a demo

```bash
git clone https://github.com/bmozi/accountable-ai-software-factory-companion.git
cd accountable-ai-software-factory-companion
./reference-factory/run-reader-journey.sh
```

The standard-library Python teaching core executes all twenty-four published
failure obligations plus one complete Work Order-to-outcome journey. It uses
SQLite and a temporary local Git effect, and requires no model provider or API
key.

Read [`START-HERE.md`](START-HERE.md) for the first laboratory path and
[`BOOK-TO-COMPANION-MAP.md`](BOOK-TO-COMPANION-MAP.md) for the complete
chapter-to-artifact curriculum. Use [`INDEX.md`](INDEX.md) to choose a
role-based, chapter-based, implementation, or failure-laboratory path. Readers
who do not use Git can download the versioned bundle from the
[latest release](https://github.com/bmozi/accountable-ai-software-factory-companion/releases/latest).

## What is here

| Path | Reader value |
|---|---|
| [`INDEX.md`](INDEX.md) | Outcome-based map of the complete premium companion. |
| [`implementation/`](implementation/) | End-to-end minimum viable accountable factory construction guide. |
| [`reference-factory/`](reference-factory/) | Vendor-neutral domain contracts, authority and evidence boundaries, recovery protocol, canonical fictional trace, twenty-four acceptance obligations, and runnable teaching code. |
| [`accountable_factory/`](accountable_factory/) and [`policies/`](policies/) | One canonical implementation and explicit admission/authority policy shared by the CLI, validator, examples, and tests. |
| [`integrations/`](integrations/) | Copyable GitHub Actions gates and deployment boundaries. |
| [`benchmarks/`](benchmarks/) | A comparative-pilot recorder that refuses to rank missing or invented observations. |
| [`schemas/`](schemas/) and [`tools/`](tools/) | Machine-readable Work Order, evidence, receipt, and outcome contracts with a dependency-free validator. |
| [`examples/`](examples/) | Complete Meridian Ledger decision trace and valid or deliberately invalid records. |
| [`exercises/`](exercises/) | Twelve failure-injection drills with explicit safe-pass conditions. |
| [`study-guides/`](study-guides/) and [`learning-paths/`](learning-paths/) | Applied workbook, eighteen deeper chapter guides, and role-specific or ninety-day routes. |
| [`diagrams/`](diagrams/) | Five editable Mermaid architecture and recovery views for workshops. |
| [`merlin/`](merlin/) | Nine sanitized first-party Merlin pattern cards with evidence limits and proof obligations. |
| [`assessment/`](assessment/) and [`decisions/`](decisions/) | Thirty-question responsibility diagnostic and ten reversible architecture-decision starters. |
| [`leadership/`](leadership/) and [`workforce/`](workforce/) | Build-versus-buy, enterprise decision-rights, AI practice, formation, and guardrail instruments. |
| [`companion/`](companion/) | Stable artifact paths named by the published Book 3. |
| [`templates/`](templates/) | Eighteen instruments covering factory charter, Work Orders, exploration, stakeholder adoption, memory governance, capacity and tenant fairness, risk-to-evidence, decision rights, human judgment, maturity, outcomes, operations, economics, threat modeling, comparative pilots, improvement, architecture choice, and the first ninety days. |
| [`MERLIN-PUBLIC-LESSONS.md`](MERLIN-PUBLIC-LESSONS.md) | Sanitized first-party failure lessons, evidence limits, and the responsibility-level architecture they changed. |
| [`PUBLIC-IMPLEMENTATIONS-TO-STUDY.md`](PUBLIC-IMPLEMENTATIONS-TO-STUDY.md) | A responsibility-by-responsibility map of public agent and software-factory projects. |
| [`BOOK-TO-COMPANION-MAP.md`](BOOK-TO-COMPANION-MAP.md) | The required reading, laboratory artifact, and proof-of-learning relationship for Chapters 3–18. |
| [`EDITION-MAP.md`](EDITION-MAP.md) | Companion version relationship to Kindle and print editions. |
| [`ERRATA.md`](ERRATA.md) | Confirmed corrections and their disposition. |

## What this is—and is not

This is a substantial, executable teaching system. It demonstrates selected
accountability invariants and supplies a construction curriculum; it is not a
production starter kit, benchmark, certification, or claim of safety. Readers
must select and operate their own identity, policy, storage, execution,
verification, source-control, delivery, and observability systems.

The repository can show that a test stopped an unsafe transition. It cannot,
by itself, teach whether the policy is legitimate, whether the evidence is
proportionate, whether a human reviewer has the competence and authority to
accept the consequence, or whether a favorable output justified the continuing
obligation. Those are book-level decisions. Treating the code as the complete
method produces exactly the component-first failure the book is designed to
prevent.

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

Executable Python and shell code under `accountable_factory/`, `benchmarks/`,
`reference-factory/example/`, `reference-factory/run-reader-journey.sh`,
`scripts/`, and `tools/` is MIT licensed.
Written content, templates, schemas, contracts, exercises, and explanatory
material are CC BY-NC-SA 4.0.
See [`LICENSE`](LICENSE), [`LICENSE-CODE`](LICENSE-CODE), and
[`LICENSE-CONTENT`](LICENSE-CONTENT). The
[`COMMERCIAL-USE.md`](COMMERCIAL-USE.md) guide explains the boundary in plain
language; the license files remain authoritative.

© 2026 John Briggs
