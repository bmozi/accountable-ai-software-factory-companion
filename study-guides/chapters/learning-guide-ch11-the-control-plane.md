# Learning Guide — Chapter 11: The Control Plane

> **Learning Objectives** — After completing this chapter, you will be able to:
>
> 1. Define the authority and enforcement responsibilities of a control plane.
> 2. Analyze permissions, protected boundaries, approvals, and exceptions separately.
> 3. Evaluate control failure and break-glass recovery paths.
> 4. Construct an authority map with independently enforced boundaries.

## Study Guide

### Key Terms

- **Control plane:** The mechanisms that govern authority and protected boundaries.
- **Protected boundary:** A consequential limit enforced outside ordinary reasoning.
- **Approval floor:** A decision that automation cannot waive or lower.
- **Exception:** A visible, bounded deviation from normal policy.
- **Break glass:** Predefined emergency authority with heightened trace and review.

### Review Questions

1. Why are prompt guardrails insufficient for material authority?
2. Which permissions should be modeled separately?
3. Why must exceptions remain noticeable?
4. Who should control changes to the control plane?

### Discussion Questions

1. Which approval floors should remain human even as evidence improves?
2. How can break-glass access be fast without becoming a hidden normal path?

### Exercises

**Exercise 11.1 (Core): Map authority.** List read, tool, write, environment, communication, merge, deploy, memory, and policy permissions.
*Deliverable:* An authority matrix.
*Assessment:* Each permission names enforcement, owner, and expansion evidence.

**Exercise 11.2 (Core): Trace an exception.** Model request, approval, scope, expiration, and retrospective review.
*Deliverable:* An exception receipt.
*Assessment:* The deviation is bounded, attributable, reversible, and visible.

**Exercise 11.3 (Challenge): Test control-plane recovery.** Simulate one control mechanism becoming unavailable or incorrect.
*Deliverable:* A degraded-mode and recovery plan.
*Assessment:* The design fails closed where consequence demands it and preserves an authorized recovery route.
