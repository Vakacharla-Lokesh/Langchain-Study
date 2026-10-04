---
tags: [n8n, lab, tier1, schedule]
difficulty: 2
time: 60 min
---
# L03 - Scheduled Digest

**Goal:** Run a workflow on a timer and produce a summary.

**Concepts:** Schedule Trigger, cron expressions, Code node, timezone handling.

## Steps
1. Add a **Schedule Trigger** set to every weekday at 09:00 in `Asia/Kolkata`.
2. Add an **HTTP Request** that fetches a public JSON feed. Try `https://api.github.com/repos/n8n-io/n8n/releases/latest` or any public API your VM can reach.
3. Add a **Code** node in *Run Once for All Items* mode that builds a one-line summary and returns it as `{ json: { summary } }`.
4. Add a final **Edit Fields** node that formats the date with `{{ $now.format('dd LLL yyyy') }}`.
5. Set the workflow to run on the schedule and check the next execution time.

> [!hint]- Hint 1
> Inside the Code node, read the upstream data with `$input.first().json`.

> [!hint]- Hint 2
> A common timezone bug is the VM running in UTC. Set the workflow timezone in Settings, not only the trigger.

## Stretch
Replace the timer with a **Wait** node, then compare the two designs in your reflection.

## Reflection
- What changes if the schedule fires while the VM is restarting?
