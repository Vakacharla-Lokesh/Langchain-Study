---
tags: [n8n, lab, tier2, loops]
difficulty: 3
time: 75 min
---
# L07 - Loops and Batching

**Goal:** Process a large list safely without overloading an API.

**Concepts:** Loop Over Items (Split in Batches), batch size, Wait node, rate limits, reset loops.

## Steps
1. Generate 50 items with a Code node.
2. Add a **Loop Over Items** node with batch size 10.
3. Inside the loop, add a **Wait** node of 1 second, then a Code node that transforms each batch.
4. Loop the output back to the Loop node until it completes.
5. After the loop, add one final node that counts processed items.

> [!hint]- Hint 1
> The "done" output of Loop Over Items only fires after all batches complete. Wire your summary there, not to the loop body.

> [!hint]- Hint 2
> If the loop never ends, check that the last node connects back to the Loop node's input.

## Stretch
Simulate an API error on batch 3 and make the loop continue with a `failed: true` flag rather than stopping.

## Reflection
- How would you choose a batch size for an API with a rate limit of 60 requests per minute?
