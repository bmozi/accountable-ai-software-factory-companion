# Merlin Software Factory — Publication-Safe Engineering Lessons

**Evidence class:** first-party historical and design lessons, not a comparative
benchmark or claim of organization-scale superiority

Merlin Software Factory is the author's private implementation and one source
of the book's architecture. This note publishes the smallest useful form of
selected lessons: the failure, the architectural decision it changed, the
reader-facing invariant, the evidence retained, and the evidence unavailable.
It does not disclose private prompts, credentials, protected paths, security
mechanisms, customer information, or reconstructable production topology.

## One accountable arc before a fleet

An earlier multi-stage direction preserved useful specialist checks but
introduced repeated context transfer, ownership ambiguity, and integration
cost. Merlin's preferred direction moved toward one accountable owner for the
complete work arc, with bounded parallel assistance only for genuinely
independent work and independent challenge.

**Reader invariant:** delegation may transfer labor; it does not transfer
consequence ownership. Every child receives explicit scope, authority, budget,
lineage, cancellation behavior, result schema, and an integrating owner.

**Evidence available:** implementation history and architectural decision
records show the change in direction.  
**Not available:** a controlled comparison proving one topology universally
faster, safer, or cheaper.

## A small endpoint exposed a factory-sized recovery defect

In May 2026, a dogfood Work Order to add a small `robots.txt` endpoint exposed
child-process cleanup and pipeline-resumption failures. The contemporaneous
record identified twenty-one Work Orders stranded in transient states and
eight follow-up defects. A retry tick could awaken without making stranded
states eligible for a new owner.

The distinction changed the recovery contract. Activity is not recovery. A
restart must reconcile every durable nonterminal state with execution reality,
restore or explicitly disposition ownership, and preserve uncertainty rather
than fabricate completion.

The same work exposed a semantic-continuity defect: a later partial structured
result could replace an earlier fuller result and temporarily erase file-scope
constraints needed downstream. Restart safety therefore includes preservation
of the admitted semantic boundary, not merely process liveness.

**Reader invariants:**

1. Every durable nonterminal record has one reclaim, reattach, terminalize, or
   escalate path.
2. Unknown external effects become `INDETERMINATE`, never automatic failure or
   success.
3. A replacement attempt receives a new identity and retains lineage to the
   interrupted attempt.
4. Retry is allowed only after reconciliation or under a preclassified,
   idempotent operation contract.
5. Structured results may not narrow admitted constraints through accidental
   replacement.

**Evidence available:** Git history, the produced change, follow-up Work Order
records, and later repair commits.  
**Not available:** the complete modern receipt, original database snapshot,
attempt-scoped cost, approval ledger, population denominator, or independently
measured business outcome. Those fields remain `not_available`.

## Local testability must preserve the contract

A hidden external dependency prevented complete local traversal of paths where
later controls and learning were expected to operate. A test double that only
returns success can therefore create false confidence. The simulation must
preserve identities, state transitions, evidence production, failures,
indeterminate effects, and recovery behavior.

**Reader invariant:** a provider substitute is credible only when the same
contract and failure obligations remain observable.

## The publication-safe responsibility map

The durable contribution is not Merlin's private directory structure. It is
the separation of responsibilities that prevents one probabilistic component
from manufacturing its own permission or evidence:

```text
intent and admission
        ↓
durable Work Order ledger ──→ independently governed control
        ↓                              ↓ grant / deny / revoke
bounded execution owner ───→ effectful adapters
        ↓                              ↓ durable operation identity
immutable candidate ───────→ criterion evidence
        ↓                              ↓ disagreement preserved
human disposition ─────────→ controlled release
        ↓
outcome observation ───────→ governed learning proposal
        ↓                              ↓ no self-promotion
reconciliation and continuing ownership
```

Readers can implement these seams with the technologies appropriate to their
environment. The executable teaching core in `reference-factory/` demonstrates
selected invariants without pretending to reproduce Merlin.
