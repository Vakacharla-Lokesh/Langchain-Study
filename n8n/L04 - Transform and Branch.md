---
tags: [n8n, lab, tier1, logic]
difficulty: 2
time: 75 min
---
# L04 - Transform and Branch

**Goal:** Route items down different paths based on their data.

**Concepts:** IF node, Switch node, Merge node, data shape, expressions with conditions.

## Scenario
You receive a list of support tickets. High-priority tickets go to one path, billing tickets to another, and everything else to a default path.

## Steps
1. Use a Manual Trigger with a Code node that returns 6 sample tickets, each with `id`, `subject`, `priority` (low/medium/high), and `category` (billing/bug/other).
2. Add a **Switch** node on `category` with outputs for `billing`, `bug`, and a fallback.
3. On the `billing` output, add an **IF** node: if `priority` equals `high`, send to "Escalate" (an Edit Fields node that sets `route: "escalate"`). Otherwise `route: "queue"`.
4. Use a **Merge** node (Append mode) to rejoin all branches.
5. Add a final Code node that counts items per route.

> [!hint]- Hint 1
> IF comparisons are strict on type. A string `"high"` and a number are not equal.

> [!hint]- Hint 2
> After a Merge, `$json` only holds the fields from one input. Reference other branches with `$('Node Name').all()`.

## Checkpoint
- Every ticket appears exactly once in the merged output, and the route counts add up to 6.

## Stretch
Replace the Switch with a single Code node that does the same routing. Write a short reflection comparing readability, testability, and how each option scales.

## Reflection
- When is a Switch clearer than nested IFs, and when is it not?
