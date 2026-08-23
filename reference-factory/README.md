# Build the Reference Accountable Factory

**Version:** 1.1
**Relationship:** implementation companion to Chapters 3–18
**Boundary:** vendor-neutral teaching contracts; not production code and not a
description of any private factory

This module turns the book's operating model into a construction exercise. The
target is a functional minimum viable factory for one frequent, reversible
software work class. Readers choose their own language, model provider, source
control, policy engine, CI system, and deployment environment.

## Run the complete teaching journey

From the repository root:

```bash
./reference-factory/run-reader-journey.sh
```

The command proves all twenty-four published failure obligations and walks the
fictional Meridian Ledger case through admission, bounded execution,
independent evidence, human disposition, a deliberately lost release response,
effect reconciliation, a canonical receipt, outcome observation, and governed
learning. It creates exactly one effect in a temporary local Git repository.

> Read the architecture. Run the failure. Change the contract. Build your first
> bounded factory.

“Read the architecture” means reading the paired book chapter, not inferring a
complete operating model from function names. Use the
[`BOOK-TO-COMPANION-MAP.md`](../BOOK-TO-COMPANION-MAP.md) curriculum before
altering a responsibility or widening authority.

## What you will build

By the end, the implementation can:

- admit or refuse versioned work;
- lease a bounded attempt to one accountable execution owner;
- preserve candidates and side effects by digest and operation identifier;
- collect criterion-level evidence from authorized sources;
- require an explicit disposition before release;
- restart without turning uncertain effects into blind retries;
- observe primary outcomes and countermetrics;
- propose learning that has no influence until separately admitted.

## Recommended build order

1. Read `01-domain-and-state-contract.md` and implement durable storage plus
   compare-and-set transitions.
2. Implement `02-execution-authority-and-evidence.md` around one execution
   adapter and one deterministic verifier.
3. Implement `03-recovery-and-reconciliation.md`; perform the crash drills
   before adding broader authority.
4. Walk `04-canonical-proof-trace.md` end to end.
5. Automate `05-acceptance-test-suite.md` in your stack.
6. Add delegation or governed improvement only after the single-owner loop
   passes every applicable test.

The canonical standard-library implementation lives in
[`accountable_factory/`](../accountable_factory/). The `example/` directory is
the executable curriculum: a compatibility import, the complete journey, and
one named test for every obligation. Schemas, CLI, validator, examples, and
tests all consume the same model.

Inspect the CLI:

```bash
PYTHONPATH=. python3 -m accountable_factory.cli journey
PYTHONPATH=. python3 -m accountable_factory.cli validate examples/artifacts/work-order.valid.json
```

Or run the journey in a disposable container:

```bash
docker build -f reference-factory/Dockerfile -t accountable-factory-reader .
docker run --rm accountable-factory-reader
```

## Deliberate omissions

This companion does not prescribe private prompts, internal routing logic,
security implementation details, production topology, or a tool inventory. It
specifies observable contracts and invariants so readers can make appropriate
technology choices without confusing one implementation with the architecture.

## Definition of done

The reference factory is complete only for the work class, authority envelope,
and environments it declares. A green demonstration is insufficient. Preserve
the evidence from at least one refusal, one failed criterion, one interruption,
one duplicate operation, one human disposition, and one mixed or inconclusive
outcome.
