# Sanitized Merlin Pattern Cards

Merlin Software Factory is the author's first-party production-system project.
These cards disclose transferable architecture lessons, not its private prompts,
credentials, protected paths, deployment topology, customer information, or
exploitable controls. “Tested foundation” means a bounded implementation or
test supports the mechanism; it does not claim organization-wide outcome
superiority.

## Card 1 — One owner for the complete arc

**Failure pressure:** A many-agent pipeline divided work cleanly on paper while
handoffs diluted intent, multiplied latency, and made integration ownership
ambiguous.

**Pattern:** Prefer one primary owner for the complete implementation arc. Add
bounded children for genuinely parallel investigation or independent review;
the parent retains shared budget, cancellation, integration, and final
evidence responsibility.

**Proof obligations:** every child has a parent attempt, reduced authority,
declared budget, result contract, cancellation behavior, and attributable
events. The integrating owner cannot disappear when work is delegated.

**Evidence boundary:** Merlin contains tested single-owner and bounded-delegation
foundations. Relative outcome advantage across work classes remains an
experimental question.

## Card 2 — Durable intent outside the session

**Failure pressure:** Long-running work crosses model contexts, processes,
people, and restarts. A transcript is neither authoritative state nor a stable
contract.

**Pattern:** Store the desired state, criteria, prohibitions, ownership,
authority, budgets, and status in a durable Work Order. Treat messages as
events or evidence, not as the only source of truth.

**Proof obligations:** a restarted worker can reconstruct the next legal action
without the prior model context; stale writers cannot overwrite a newer state;
every transition is attributable.

**Evidence boundary:** Merlin's durable Work Order and guarded-transition tests
support the mechanism. They do not prove that any particular schema captures a
legitimate business promise.

## Card 3 — Separate desired state from convergence

**Failure pressure:** Imperative orchestration can mistake an interrupted
command for unfinished work and repeat effects.

**Pattern:** Reconcile observed state toward declared desired state. Make the
next action a consequence of authoritative records, not the memory of a worker.

**Proof obligations:** repeated reconciliation is safe; ownership of a lease or
attempt is explicit; observation distinguishes absent, present, partial, and
indeterminate effects.

**Evidence boundary:** Merlin has tested control-loop foundations. Distributed
recovery across every provider and failure mode remains deployment-specific.

## Card 4 — The receipt is part of the product

**Failure pressure:** A generated artifact can look complete while hiding the
intent, authority, evidence, dissent, or release decision that justified it.

**Pattern:** Produce an attributable factory receipt linking the exact artifact
to intent, attempts, evidence, disposition, external effects, and outcome
obligations.

**Proof obligations:** child attempts remain attributable; evidence names the
candidate digest; the release actor and exposure are explicit; the record
survives restart.

**Evidence boundary:** Merlin has contract and conformance tests for selected
receipt relationships. Completeness for a regulated domain still requires
local legal, risk, and records review.

## Card 5 — Bound retry and repair separately

**Failure pressure:** A retry loop can convert one fault into uncontrolled cost,
duplicate effects, or repeated production of the same invalid candidate.

**Pattern:** Distinguish transport retry, repair iteration, and policy
reconsideration. Give each a separate budget and stopping rule. Reconcile
effectful operations before retry.

**Proof obligations:** concurrent attempts conserve one shared budget; repeated
no-change repair stops; lost responses become indeterminate; a retry cannot
mint new authority.

**Evidence boundary:** Merlin's cost guards, bounded repair behavior, and
reconciliation tests provide tested foundations. Tail behavior under provider
outage and organization-scale load still requires drills.

## Card 6 — Fan-out must conserve authority and capacity

**Failure pressure:** Parallel workers can each observe the same remaining
budget or permission and collectively exceed it.

**Pattern:** Reserve scarce capacity atomically before launch. Child authority
is a subset of the parent grant. Record the binding constraint and preserve one
integration owner.

**Proof obligations:** no child can broaden tools, data, environment, or spend;
cancelled work releases only unused reservation; tenant fairness and reviewer
capacity participate in admission.

**Evidence boundary:** Merlin has bounded fan-out and resource-aware design
foundations. Fairness, provider quotas, and distributed reservation need
validation in the reader's infrastructure.

## Card 7 — Memory must pass through influence states

**Failure pressure:** A useful observation can become retrieved guidance and
then de facto policy without independent testing, scope, or expiry.

**Pattern:** Separate record, observation, candidate learning, validated
practice, and retired learning. Govern provenance, reinforcement,
contradiction, decay, and retrieval eligibility.

**Proof obligations:** similarity cannot grant authority; expired or
out-of-scope learning cannot change behavior; contradictions remain visible;
promotion requires a separate authorized decision.

**Evidence boundary:** Merlin has provenance-aware memory and learning-state
foundations. The effectiveness and bias of long-lived organizational memory
remain open empirical questions.

## Card 8 — Improvement cannot change its own judge

**Failure pressure:** A self-improving factory can optimize activity, weaken
tests, or expand authority to make its own results look better.

**Pattern:** Improvement may observe, propose, and run a bounded experiment. It
cannot approve persistent influence, weaken the evidence floor, or expand its
own authority.

**Proof obligations:** baseline and countermetric are declared before results;
proposal and evaluator are separable; rollback and expiry are mandatory;
negative and inconclusive results survive.

**Evidence boundary:** Merlin has proposed, tested, and rejected improvement
paths that support the protected-boundary pattern. Long-term transferred
outcome benefit is not yet established.

## Card 9 — Operator visibility is a control surface

**Failure pressure:** A system can be technically observable while operators
cannot tell what is stuck, why it stopped, what it may still do, or who can
intervene.

**Pattern:** Expose work state, budget, authority, binding constraint,
evidence status, human decision, and recovery options in operator language.
Define read-only, draft-only, drain, constrained, and stopped modes.

**Proof obligations:** every stop has a reason and next owner; absence behavior
is explicit; a degraded mode cannot silently lower the evidence floor.

**Evidence boundary:** Merlin's operator and status-projection tests support
selected visibility mechanics. Whether operators understand and trust them
requires observation with real users.

## How to use a card

For one card, write:

1. the local failure pressure;
2. the smallest work class where it applies;
3. the deterministic mechanism that enforces it;
4. the unhappy-path test;
5. the human decision that remains;
6. the evidence that would contradict the pattern; and
7. the date or event that forces review.

Do not copy a pattern because Merlin uses it. Adopt it only when your local
failure, authority, and evidence justify it.
