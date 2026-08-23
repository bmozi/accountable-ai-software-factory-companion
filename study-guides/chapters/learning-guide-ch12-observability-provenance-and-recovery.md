# Learning Guide — Chapter 12: Observability, Provenance, and Recovery

> **Learning Objectives** — After completing this chapter, you will be able to:
>
> 1. Distinguish observability, provenance, reproducibility, and recovery.
> 2. Analyze partial completion before and after consequential side effects.
> 3. Evaluate whether a receipt supports explanation, resumption, and rollback.
> 4. Construct a minimum viable trace for one production effect.

## Study Guide

### Key Terms

- **Observability:** Visibility into state sufficient to support an operational decision.
- **Provenance:** Durable lineage of inputs, actions, evidence, and decisions.
- **Receipt:** A structured record of what happened under which authority.
- **Partial completion:** Work that stopped after producing some state or consequence.
- **Reconciliation:** Establishing actual state before selecting a recovery action.

### Review Questions

1. Why is provenance not the same as reproducibility?
2. Which links belong in a minimum viable trace?
3. Why must recovery distinguish pre-effect and post-effect interruption?
4. How can incidents improve the factory contract?

### Discussion Questions

1. Which trace data is necessary, and which creates avoidable privacy or cost?
2. When should recovery prefer compensation over resumption?

### Exercises

**Exercise 12.1 (Core): Build a minimum trace.** Link one production effect backward through work order, intent, artifact, evidence, authority, approval, and actor.
*Deliverable:* A provenance trace.
*Assessment:* Every consequential link is durable and attributable.

**Exercise 12.2 (Core): Classify partial completion.** Model interruption before and after a side effect.
*Deliverable:* Two recovery receipts.
*Assessment:* Each receipt names actual state, safe options, and owner.

**Exercise 12.3 (Challenge): Reconcile a restart.** Introduce stale local state and an uncertain external effect.
*Deliverable:* A reconciliation procedure.
*Assessment:* The procedure verifies reality before retry, resume, compensate, or stop.
