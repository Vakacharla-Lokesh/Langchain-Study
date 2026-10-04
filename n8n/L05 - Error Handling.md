---
tags: [n8n, lab, tier1, reliability]
difficulty: 3
time: 75 min
---
# L05 - Error Handling

**Goal:** Make a workflow fail gracefully and alert you when it does.

**Concepts:** Error Trigger workflow, node setting "On Error: Continue", retry on fail, execution logs.

## Steps
1. Build a workflow with an **HTTP Request** to a URL that you deliberately break, such as `https://httpstat.us/500` or a typo'd domain.
2. In the HTTP node settings, enable **Retry On Fail** with 3 tries and a 2-second wait. Observe the retries in the execution log.
3. Set the node's **On Error** option to *Continue (using error output)*, then route the error output to an Edit Fields node that records the failure.
4. Create a second workflow that starts with an **Error Trigger**. Point the first workflow's settings to use it as its error workflow. Have it send yourself a message or write a row to a log sheet.

> [!hint]- Hint 1
> Error workflows only fire for failed production executions, not manual test runs.

> [!hint]- Hint 2
> Retries and continue-on-error solve different problems. Retries handle transient failures, and continue-on-error keeps the rest of the batch alive.

## Checkpoint
- A deliberately failing call produces an error log entry and triggers the error workflow.

## Reflection
- Which failures should retry, and which should stop the whole workflow?
