---
tags: [n8n, lab, tier1]
difficulty: 1
time: 30 min
---
# L01 - Hello Workflow

**Goal:** Build and run your first workflow, then inspect every item.

**Concepts:** triggers, nodes, executing a single node, reading output.

## Steps
1. Create a new workflow and name it `L01 Hello`.
2. Add a **Manual Trigger**.
3. Add an **Edit Fields (Set)** node. Add three fields: `name` (your first name), `timestamp` (`{{ $now.toISO() }}`), and `mood` (a word you pick).
4. Add a second **Edit Fields** node that creates `message` as `Hi {{ $json.name }}, your mood is {{ $json.mood }}`.
5. Execute the workflow and open each node's output.
6. Duplicate the workflow, then change the first node to produce three items instead of one.

> [!hint]- Hint 1
> Use Manual Trigger's "Execute Workflow" button, not the node-level play button, to run the whole graph.

> [!hint]- Hint 2
> For step 6, use a Code node with `return [{json:{name:'A'}},{json:{name:'B'}},{json:{name:'C'}}];` in place of the trigger output.

## Checkpoint
- Three items flow through the second node, and each gets its own `message`.

## Stretch
Pin the data on the first node and explain in your reflection what pinning does and why it saves API calls.

## Reflection
- What did an item look like in the output panel?
