# Build the Reference Accountable Factory

**Version:** 0.2
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

The command runs the failure-oriented tests and walks the fictional Meridian
Ledger case through exploration, admission, bounded execution, evaluator-
independence refusal, conflicting evidence, human disposition, indeterminate
release, restart reconciliation, provider substitution, mixed outcome,
narrowed authority, rejected learning, and prototype retirement.

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

The `example/` directory contains a small standard-library Python teaching core
with executable tests. It demonstrates selected invariants; it is a scaffold,
not a production starter kit.

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
