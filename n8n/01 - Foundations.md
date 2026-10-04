---
tags: [n8n, concepts, foundations]
---
# 01 - Foundations

## The Mental Model
A **workflow** is a directed graph. Each **node** does one job. Data moves between nodes as **items**, which are JSON objects, always delivered as an array. Most confusion in n8n comes from forgetting that every node receives a list of items and runs once per item unless it is told otherwise.

## Core Concepts

**Triggers** start a workflow: Manual Trigger, Schedule Trigger, Webhook, and app triggers such as a new row in a sheet. Every workflow needs exactly one starting point.

**Regular nodes** transform, call, or route data. Examples include HTTP Request, Edit Fields, Code, IF, and Switch.

**Items** look like this:
```json
[
  { "json": { "name": "Asha", "score": 82 } },
  { "json": { "name": "Ravi", "score": 47 } }
]
```
In the UI you usually see only the `json` part.

**Expressions** pull values from earlier nodes:
```
{{ $json.name }}                      // current node's input item
{{ $json.body.email }}                // webhook payload lives under body
{{ $('Webhook').item.json.body.id }}  // value from a named upstream node
{{ $now.toISO() }}                    // current time
```

**Credentials** are stored encrypted in n8n and referenced by name. You should never type a secret into a node field.

**Execution** can be inspected per node in the Executions panel. Reading that panel is your main debugging tool.

## Concept Checks (try before reading on)
1. If a node receives 5 items and you use `{{ $json.name }}` in an HTTP Request, how many requests fire?
2. Why does a webhook payload need `.body` in its expression path?
3. Where do you go to see the exact input a node received on its last run?

> [!answer]- Answers
> 1. Five, one per item, unless the node is set to run once.
> 2. The webhook node wraps the request as `headers`, `query`, `body`, and so on.
> 3. The execution log for that node, which shows its input and output.

## Stepping Stone
Build a throwaway workflow: Manual Trigger → Edit Fields that adds a field called `greeting` → a second Edit Fields that uses `{{ $json.greeting }}`. Run it, and open each node's output to watch the data change.
