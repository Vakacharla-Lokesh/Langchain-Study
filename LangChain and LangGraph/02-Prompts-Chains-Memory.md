---
tags: [langchain, prompts, memory, chains]
prev: "[[01-LangChain-Fundamentals]]"
next: "[[03-Tool-Calling-and-Function-Calling]]"
---

# 02 — Prompts, Chains & Memory

## Theory

### Prompt Templates
`PromptTemplate` (string-based) and `ChatPromptTemplate` (message-based) let you parameterize prompts instead of f-string hacking.

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful {domain} assistant."),
    ("human", "{question}")
])
```

Key variants:
- `MessagesPlaceholder("history")` — reserves a slot in the template where a *list* of prior messages gets injected. This is the mechanism memory and agent scratchpads plug into.
- `FewShotPromptTemplate` — injects example input/output pairs before the real query, useful for steering format/tone without fine-tuning.

### Chains (the pre-agent way of composing logic)
A "chain" is any fixed sequence of Runnables. Two flavors matter for the agent path ahead:
- **Sequential chains** — output of step N feeds step N+1 (`prompt | model | parser`)
- **Router chains / branching** — pick which sub-chain to run based on a classification step. This is the *manual, hardcoded* version of what an agent does dynamically. Understanding this makes ReAct agents click faster — an agent is essentially "a router chain where the LLM is the router, and it can route in a loop, not just once."

### Memory — why it's tricky
LLM calls are stateless. "Memory" in LangChain just means: **you keep a running list of messages and re-send the relevant ones on every call.** There is no persistent hidden state inside the model.

Modern approach (LangChain has deprecated the old `ConversationBufferMemory` class family in favor of manual state management, which — not coincidentally — is exactly what LangGraph's `State` + checkpointer gives you):

| Strategy | What it does | Tradeoff |
|---|---|---|
| Buffer (keep everything) | Append every message, resend all | Simple, but blows the context window fast on long sessions |
| Windowed buffer | Keep only last *k* turns | Cheap, but forgets anything older than the window |
| Summarization | Periodically compress old turns into a running summary via an LLM call | Saves tokens, but summary can drop details / costs an extra LLM call |
| Vector-store retrieval memory | Store past turns as embeddings, retrieve only relevant ones per query | Scales to huge history, but retrieval quality now gates recall |
| **Checkpointed graph state (LangGraph)** | State object persists automatically per `thread_id` | The modern default — see Lesson 06 |

**Important point:** for agent work specifically, memory doubles as the **agent's scratchpad** — the growing list of `(Thought, Action, Observation)` steps *within a single task* is also "memory," just short-lived. Don't mentally separate "conversation memory" from "agent reasoning trace" — in LangGraph they're often the same `messages` list in State.

## Important Points
- `ChatPromptTemplate.from_messages` is what you'll use 95% of the time — prefer it over raw string formatting so variable substitution is validated.
- Order in `MessagesPlaceholder` matters: system prompt → history → new human input → (for agents) scratchpad. Get the order wrong and the model loses track of what's "current."
- Token budget is a real constraint you'll hit in labs — always know your model's context window and roughly how memory strategy affects it.
- Summarization memory introduces an LLM call *before* your main call — factor that into latency/cost estimates for anything you build.

## Course Mapping
> Fill in: Section/Lecture covering PromptTemplates, ConversationBufferMemory, memory types.

## Research/Reference
- No single paper; conceptually related to "context management" discussions in longer-context agent papers (will resurface in Lesson 04/06).
- Docs: python.langchain.com → "How to" → Memory / Prompts sections.

## Hands-on Labs
- **Easy:** Build a `FewShotPromptTemplate` with 3 examples that makes the model always respond in a fixed JSON shape, without using structured output — just prompting discipline.
- **Medium:** Implement windowed memory manually (keep last 4 messages only) in a chat loop and demonstrate that the model "forgets" something said 6 turns ago.
- **Hard:** Implement summarization memory: every 5 turns, fire a separate LLM call that compresses the conversation so far into a 3-sentence summary, replace the old messages with that summary + last 2 raw turns. Log token counts before/after to prove the savings.

---
⬅ [[01-LangChain-Fundamentals]] | ➡ [[03-Tool-Calling-and-Function-Calling]]
