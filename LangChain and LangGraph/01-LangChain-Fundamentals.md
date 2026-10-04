---
tags: [langchain, fundamentals, lcel, runnables]
prev: "[[00-Index]]"
next: "[[02-Prompts-Chains-Memory]]"
---

# 01 — LangChain Fundamentals

## Theory

LangChain is a framework for building applications that chain together **LLM calls + external data/tools**, instead of making one-shot prompt calls. Its whole design rests on one interface:

### The `Runnable` interface
Every core building block (chat model, prompt template, output parser, retriever, tool) implements the same interface:
- `.invoke(input)` — run once, get a result
- `.batch([inputs])` — run over a list
- `.stream(input)` — get tokens/chunks as they're produced
- `.ainvoke` / `.abatch` / `.astream` — async versions

Because everything is a `Runnable`, you can **compose** them like Unix pipes.

### LCEL (LangChain Expression Language)
LCEL is just the `|` operator overloaded on `Runnable` to mean "pipe the output of the left into the input of the right":

```python
chain = prompt | model | output_parser
result = chain.invoke({"topic": "black holes"})
```

Under the hood this builds a `RunnableSequence`. LCEL also gives you, for free:
- Automatic parallelism via `RunnableParallel` (dict of runnables run concurrently)
- Streaming that propagates through the whole chain, not just the final LLM call
- Async support without rewriting anything
- Built-in retries / fallbacks (`.with_retry()`, `.with_fallbacks()`)

### Chat Models vs LLMs (legacy distinction)
- `LLM` objects: string in → string in (legacy, text-completion style, mostly deprecated for new models)
- `ChatModel` objects: list of `Message` objects in → `AIMessage` out. **This is what you should be using in 2026** — every serious provider (OpenAI, Anthropic, etc.) is chat-native now.

### Message types
- `SystemMessage` — instructions/persona, sent once
- `HumanMessage` — user turn
- `AIMessage` — model turn (can contain `tool_calls`)
- `ToolMessage` — result of a tool call, keyed to a `tool_call_id`

This message taxonomy matters a LOT once you get to agents (Lesson 03/04) — the ReAct loop is literally a growing list of these messages.

### Output Parsers
Convert raw model output into structured Python objects:
- `StrOutputParser` — just extracts `.content` as a string
- `JsonOutputParser` — parses JSON, can stream partial JSON
- `PydanticOutputParser` / `.with_structured_output(SomeModel)` — the modern, preferred way to get typed structured output (uses the model's native function-calling/JSON-mode under the hood instead of regex-parsing free text)

**Important pivot to know:** older tutorials teach `PydanticOutputParser` with format instructions injected into the prompt. Newer, more reliable approach is `model.with_structured_output(Schema)` which uses the provider's native tool-calling — far less brittle. Prefer this in anything you build now.

## Important Points
- LangChain ≠ the model. It's an orchestration layer — you still need an API key for an actual LLM provider.
- `invoke` vs `stream` vs `batch` are not cosmetic — pick based on UX (streaming for chat UIs, batch for offline processing).
- LCEL chains are declarative graphs under the hood — you can call `.get_graph().print_ascii()` on any chain to visualize it. Useful for debugging composition mistakes.
- Don't confuse **chains** (fixed, linear/parallel pipelines, no branching decisions by the LLM) with **agents** (LLM decides the next step at runtime). Chains = you hardcode the control flow. Agents = the model controls the control flow. This distinction is *the* reason LangGraph exists (branching/looping is awkward to express in pure LCEL).
- Version churn is real: LangChain has deprecated `LLMChain`, old-style `initialize_agent`, and is steadily pushing everything agent-related toward LangGraph. If a Udemy course teaches `AgentExecutor` + `initialize_agent`, treat it as "understand the concept, but know the modern implementation lives in LangGraph."

## Course Mapping
> Fill in as you go: `Section __ / Lecture __` — "LCEL basics", "Runnables deep dive", etc.

## Research/Reference
- No dedicated paper for this lesson — it's framework mechanics. Primary source: python.langchain.com "Conceptual Guide" section.

## Hands-on Labs (quick links — full detail in [[08-Hands-On-Labs]])
- **Easy:** Build a 3-step LCEL chain: prompt → model → `StrOutputParser`, that summarizes any pasted text in exactly 3 bullet points.
- **Medium:** Build a `RunnableParallel` chain that takes one topic and simultaneously generates a tweet, a LinkedIn post, and a haiku about it — all in one `.invoke()`.
- **Hard:** Build a chain with `.with_structured_output()` that takes a messy paragraph of a restaurant review and extracts a typed Pydantic object: `{sentiment, dishes_mentioned: list[str], rating_out_of_5}`. Add `.with_fallbacks()` to a second model in case the first fails structured parsing.

---
⬅ [[00-Index]] | ➡ [[02-Prompts-Chains-Memory]]
