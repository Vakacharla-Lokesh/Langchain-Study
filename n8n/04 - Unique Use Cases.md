---
tags: [n8n, use-cases, capstone]
---
# 04 - Unique Use Cases

Each project combines several labs. Build the stepping stones in order, and attempt each one before opening its hints.

## 1. Expense Receipt Triage
**Combines:** L02, L04, L05, L09
**Idea:** A receipt is emailed or uploaded. The workflow extracts the amount and vendor with a model, flags anything over a threshold, and logs it.
- Stepping stone 1: Hard-code one receipt's text and extract fields with a model (L09).
- Stepping stone 2: Route by amount with a Switch (L04).
- Stepping stone 3: Log to a sheet and alert on errors (L05).
> [!hint] Ask the model for strict JSON, then validate the amount is numeric before the threshold check.

## 2. Meeting Notes to Action Items
**Combines:** L02, L09, L10
**Idea:** Paste a transcript into a form. The agent extracts owner, task, and due date, then creates a row per action item.
- Stepping stone 1: Extract one action item from a sample transcript.
- Stepping stone 2: Loop over items and write each to a sheet (L07).
> [!hint] Treat the model's output as untrusted. Check for missing owners before writing.

## 3. Internal Knowledge Bot for a Team Wiki
**Combines:** L11, L12
**Idea:** A chat bot answers questions from a folder of team docs and remembers the conversation.
- Stepping stone 1: Index one document (L12).
- Stepping stone 2: Add per-user memory (L11).
> [!hint] Re-index on a schedule (L03) so answers do not go stale.

## 4. Server Health Watchdog
**Combines:** L03, L04, L05, L06
**Idea:** Every 5 minutes, call a health endpoint on the VM. If it fails twice in a row, alert and log.
- Stepping stone 1: Call the endpoint and record status (L06).
- Stepping stone 2: Keep a counter in workflow static data and alert at 2 failures.
> [!hint] Static data persists between executions. Use it for the consecutive-failure count.

## 5. Customer Feedback Sentiment Dashboard
**Combines:** L07, L09, L04
**Idea:** Nightly, classify a batch of feedback rows by sentiment and write summary counts to a sheet.
- Stepping stone 1: Classify 5 rows (L09).
- Stepping stone 2: Batch the full set with rate limiting (L07).
