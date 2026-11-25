# Follow the decision: interactive learning guide

A public, vendor-neutral reading companion for John Briggs's *The Accountable
AI Software Factory*. Version 1.0, updated 2026-11-25. Its practical benefit is
helping a reader connect an architecture question to a book chapter, an exercise
and evidence they can inspect. For example, a team reviewing a small change can
trace why corrected guidance or withdrawn permission stops further work.

Open [index.html](index.html) in a browser. No build, installation, model provider,
API key or internet connection is needed for the guide itself. Repository links
require the surrounding checkout; the canonical repository link uses the internet
only when a reader chooses it. All styling and interactions are local files.

For a loopback preview from the repository root:

```bash
python3 -m http.server 3023 --bind 127.0.0.1
```

Then visit `http://127.0.0.1:3023/diagrams/interactive-guide/`.
Stop the server after review. This command previews the checkout; it does not
publish a website or change repository visibility or crawler/training permissions.

## What to inspect

- Seven responsibility panels connect intent, context, authority, execution,
  verification, outcomes and validated learning to existing teaching resources.
- Governance crosses the entire chain; seven responsibilities do not mandate
  seven agents, runtime stages or services.
- Four **fixed conceptual scenarios** explain corrected sources, withdrawn
  permission, missing checks and candidate learning. They do not evaluate policy,
  grant authority or execute the Python laboratory.
- Five **proposed descriptive assistance levels** explain human involvement.
  They are not credentials or a numeric permission system.
- Ordinary buttons support keyboard use, visible focus and pressed state.
  Reduced motion is respected. Print styling includes all seven responsibility
  panels. With JavaScript disabled, all panels remain readable.

The separate [extended laboratory](../../reference-factory/06-context-authority-and-learning.md)
and [Python journey](../../reference-factory/example/run_context_authority_journey.py)
exercise selected mechanisms using fictional data. In the canonical teaching
factory, a missing required check prevents disposition and receipt creation;
this guide does not manufacture an incomplete canonical receipt.

## Sources, scope and corrections

The [book-to-companion map](../../BOOK-TO-COMPANION-MAP.md),
[editable architecture views](../accountable-factory-visual-guide.md),
[memory-governance workbook](../../templates/memory-governance-workbook.md)
and [reference factory](../../reference-factory/README.md) supply the public
teaching relationships. The book supplies the judgment and tradeoffs; this guide
is not a substitute for the book or a description of a private implementation.
No private implementation topology, source paths, tool inventory, customer data
or reference photographs are embedded.

The canonical public resource is this directory in the
[companion repository](https://github.com/bmozi/accountable-ai-software-factory-companion/tree/main/diagrams/interactive-guide).
No hosted HTML canonical URL is declared because no website deployment is
asserted. The repository link identifies the source; GitHub does not render this
HTML as a hosted website. No indexing submission,
AI citation, usability study, certification, production safety result or ROI
measurement is claimed. Report corrections through [errata](../../ERRATA.md)
and the repository's contribution process.

Written and presentation content, including HTML/CSS, uses
[CC BY-NC-SA 4.0](../../LICENSE-CONTENT). Executable JavaScript and the separate
Python teaching code use the [MIT code license](../../LICENSE-CODE), as identified
in their source notices.
