---
tags: [n8n, lab, tier2, modular]
difficulty: 3
time: 60 min
---
# L08 - Sub-workflows

**Goal:** Extract reusable logic into a workflow that other workflows call.

**Concepts:** Execute Workflow node, Execute Workflow Trigger, input contracts, reuse.

## Steps
1. Build workflow `Util - Normalize Contact` with an **Execute Workflow Trigger**. It accepts `name` and `email`, returns cleaned values, and uses an Edit Fields node to trim and lowercase.
2. Build workflow `Caller` with a Manual Trigger and an **Execute Workflow** node that calls the util with two different inputs.
3. Confirm the caller receives the cleaned output.

> [!hint]- Hint 1
> The sub-workflow must be saved and its trigger set to accept input data for it to appear in the caller's picker.

## Reflection
- What contract did you implicitly create between the two workflows, and what breaks if someone renames a field?
