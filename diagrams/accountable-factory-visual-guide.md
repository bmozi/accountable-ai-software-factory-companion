# Accountable Factory Visual Guide

These diagrams are conceptual, vendor-neutral teaching views. They do not
describe Merlin's production topology. GitHub renders the Mermaid sources;
copy them into any Mermaid-compatible editor for workshops.

## 1. The accountability spine

```mermaid
flowchart LR
    WO[Work Order] --> AT[Attempt]
    AT --> CA[Candidate artifact]
    CA --> EV[Evidence records]
    EV --> DI[Disposition]
    DI --> EF[External effect]
    EF --> RC[Factory receipt]
    RC --> OO[Outcome observation]
    OO --> LR[Learning or retirement decision]
    EV -. bound to exact digest .-> CA
    DI -. owned by authorized actor .-> EV
```

**Workshop question:** Which link in your present process exists only in a chat
transcript or a person's memory?

## 2. Four responsibility planes

```mermaid
flowchart TB
    D[Decision plane<br/>intent, evidence, disposition, outcomes]
    C[Control plane<br/>identity, policy, authority, budgets]
    E[Execution plane<br/>models, agents, tools, environments]
    O[Observation plane<br/>events, provenance, receipts, recovery]
    D -->|declared work and evidence floor| C
    C -->|bounded grant| E
    E -->|candidate and tool events| O
    O -->|reconstructable evidence| D
    E -. cannot grant itself authority .-> C
```

**Workshop question:** Can the execution path change the policy, evidence
requirement, or judge that controls it?

## 3. Evidence and disposition are different

```mermaid
flowchart LR
    C[Candidate digest] --> T1[Deterministic checks]
    C --> T2[Independent evaluator]
    C --> T3[Human or domain review]
    T1 --> P[Evidence package]
    T2 --> P
    T3 --> P
    P --> Q{Agreement and sufficiency?}
    Q -->|Yes| A[Authorized disposition]
    Q -->|No| X[Repair, reject, narrow, or expire exception]
```

**Workshop question:** Who can disposition disagreement, and what happens when
that person is absent?

## 4. Reconciliation before retry

```mermaid
flowchart TD
    S[Send effect with operation ID] --> R{Response received?}
    R -->|Yes| K[Record known result]
    R -->|No| I[Mark indeterminate]
    I --> Q[Query authoritative external state]
    Q -->|Effect exists| J[Reattach and complete receipt]
    Q -->|Proven absent| Y[Retry with same identity]
    Q -->|Cannot determine| H[Human repair or escalation]
```

**Workshop question:** Which of your adapters interprets a timeout as proof
that nothing happened?

## 5. Authority expands one dimension at a time

```mermaid
flowchart LR
    A[Advisory<br/>synthetic data] -->|evidence| B[Draft-only<br/>approved data]
    B -->|evidence| C[Bounded write<br/>isolated environment]
    C -->|evidence| D[Limited release<br/>small exposure]
    D -->|outcome and recovery evidence| E[Broader authority]
    E -->|harm, drift, or expiry| D
    D -->|harm or insufficient evidence| C
    C -->|control failure| B
```

**Workshop question:** Can you name the single authority dimension being
expanded and the evidence that would contract it again?
