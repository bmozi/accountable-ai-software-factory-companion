# Learning Guide — Chapter 5: Work Orders and the Decision Chain

> **Learning Objectives** — After completing this chapter, you will be able to:
>
> 1. Define a work order as a durable accountability record.
> 2. Analyze state transitions, ownership, evidence, and stale-state protection.
> 3. Evaluate handoffs and retries for loss of context or duplicated consequence.
> 4. Construct a resumable decision chain for one work class.

## Study Guide

### Key Terms

- **Work order:** The durable accountability record for a change.
- **State transition:** A governed move between named work conditions.
- **Handoff contract:** The required context, evidence, and ownership transferred between actors.
- **Stale-state protection:** A mechanism that prevents decisions against superseded artifacts.
- **Reconciliation:** Determining the true state before resuming or repeating work.

### Review Questions

1. Why is a work order more than a prompt?
2. What must accompany a handoff?
3. Why can retry be unsafe after a side effect?
4. When does an approval become stale?

### Discussion Questions

1. How much state must be durable before the coordination cost outweighs its value?
2. Which decisions in your current delivery process live only in conversation?

### Exercises

**Exercise 5.1 (Core): Model the decision chain.** List required states, inputs, owners, evidence, and permitted next states.
*Deliverable:* A state-transition table.
*Assessment:* Every consequential transition has an owner and evidence floor.

**Exercise 5.2 (Core): Audit a handoff.** Examine one real handoff for lost rationale, stale context, or unclear consequence.
*Deliverable:* A handoff contract revision.
*Assessment:* The receiving actor can decide without relying on hidden conversation.

**Exercise 5.3 (Challenge): Design restart reconciliation.** Specify recovery before and after one irreversible side effect.
*Deliverable:* A restart decision tree.
*Assessment:* The tree distinguishes retry, resume, compensate, escalate, and stop.
