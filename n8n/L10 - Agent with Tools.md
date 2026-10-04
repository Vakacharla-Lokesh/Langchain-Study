---
tags: [n8n, lab, tier3, ai, agents, tools]
difficulty: 4
time: 2 hr
---
# L10 - Agent with Tools

**Goal:** Build an agent that decides which tool to call to answer a question.

**Concepts:** AI Agent node, tool nodes, tool descriptions as routing logic, the agent loop (think, act, observe).

## Concept First
An agent is a model in a loop. On each turn it reads the conversation, chooses a tool or answers directly, reads the tool's result, and repeats. The tool's **description** is what the model uses to decide when to call it, so vague descriptions cause wrong choices.

## Steps
1. Add a **Chat Trigger** node. This gives you a built-in chat window.
2. Add an **AI Agent** node. Attach an approved chat model.
3. Attach two tools:
   - **Calculator** tool, for arithmetic.
   - A **Code** tool or an **HTTP Request** tool that returns the current date or a fixed lookup table of 5 products with prices.
4. Write a clear description for each tool. Make the product tool say when to use it: "Use this when the user asks about product prices or stock."
5. Ask three types of question: pure arithmetic, a product lookup, and a general knowledge question. Check which tool it chose each time.
6. Rename the product tool to something vague like `do_thing` and rerun the lookup question. Observe what happens.

> [!hint]- Hint 1
> If the agent never calls a tool, check the tool description and whether the model you chose supports tool calling.

> [!hint]- Hint 2
> Keep the system message short. Put the rules in tool descriptions.

## Checkpoint
- Each question routes to the right tool, and you can explain why from the descriptions.

## Stretch
Add a tool that is a sub-workflow (from L08) so the agent can call your normalization logic.

## Reflection
- How did renaming the tool change behavior, and what does that tell you about where agent logic lives?
