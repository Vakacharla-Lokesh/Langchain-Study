---
tags: [n8n, lab, tier3, ai, llm]
difficulty: 3
time: 60 min
---
# L09 - First LLM Call

**Goal:** Call a language model from a workflow and control its output.

**Concepts:** Chat model nodes, Basic LLM Chain, system vs user prompts, structured output, temperature.

> [!warning] Company policy
> Check with IT which model providers are approved. If none are, use the company's approved internal model endpoint, or skip to a local option your admin provides. Do not send confidential data to an unapproved service.

## Steps
1. Add a **Manual Trigger** and an **Edit Fields** node with a `ticket` string field containing a sample customer complaint.
2. Add a **Basic LLM Chain** node. Attach an approved chat model node as its model.
3. Write a system prompt: *You classify support tickets. Reply only with JSON: {"sentiment": "...", "urgency": 1-5, "summary": "..."}.*
4. Set the user message to `{{ $json.ticket }}`.
5. Run it five times on the same ticket and compare outputs.
6. Lower the temperature and run again. Note the change.

> [!hint]- Hint 1
> If the output includes extra prose around the JSON, tighten the system prompt and add an example of the exact shape you want.

> [!hint]- Hint 2
> Parse the reply with a Code node using `JSON.parse`, wrapped in a try/catch that routes malformed output to a fallback.

## Reflection
- Which part of your prompt did the model follow reliably, and which part did it ignore?
