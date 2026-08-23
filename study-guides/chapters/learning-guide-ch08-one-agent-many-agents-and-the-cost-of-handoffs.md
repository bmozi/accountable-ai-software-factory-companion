# Learning Guide — Chapter 8: One Agent, Many Agents, and the Cost of Handoffs

> **Learning Objectives** — After completing this chapter, you will be able to:
>
> 1. Compare single-agent, staged, parallel, and owner-led fan-out designs.
> 2. Analyze handoff cost, context loss, independence, and integration risk.
> 3. Evaluate when bounded delegation improves a production arc.
> 4. Construct an evidence-based orchestration decision for one work class.

## Study Guide

### Key Terms

- **Orchestration:** Coordination of actors, state, handoffs, and decisions.
- **Owner-led fan-out:** Bounded delegation under one accountable production owner.
- **Handoff cost:** Context, time, and error introduced by transferring work.
- **Independent challenge:** Evaluation using a reasoning path distinct from production.
- **Attribution:** Durable linkage between an action, actor, evidence, and parent work.

### Review Questions

1. What context advantage can one agent preserve?
2. Which benefits can multiple agents provide?
3. Why is parallelism not automatically better orchestration?
4. How does owner-led fan-out preserve accountability?

### Discussion Questions

1. When is independent challenge worth an additional handoff?
2. Should child work ever be allowed to outlive its parent work order?

### Exercises

**Exercise 8.1 (Core): Compare designs.** Score single, staged, parallel, and owner-led designs for one work class.
*Deliverable:* An orchestration decision matrix.
*Assessment:* The selected design follows a named constraint and reversal condition.

**Exercise 8.2 (Core): Specify a child contract.** Define scope, tools, quota, evidence, return format, cancellation, and attribution.
*Deliverable:* A bounded delegation contract.
*Assessment:* The child cannot silently expand authority or lose parent lineage.

**Exercise 8.3 (Challenge): Test steering and recovery.** Interrupt, redirect, and resume a simulated child while preserving one decision chain.
*Deliverable:* An event-and-reconciliation trace.
*Assessment:* Follow-up, cancellation, state, budget, and result ownership remain unambiguous.
