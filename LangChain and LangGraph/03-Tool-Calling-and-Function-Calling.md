---
tags: [langchain, tools, function-calling]
prev: "[[02-Prompts-Chains-Memory]]"
next: "[[04-ReAct-Agents-Theory-and-Papers]]"
---

# 03 — Tool Calling & Function Calling

## Theory

This is the lesson everything after it depends on. **An agent is nothing more than: a model that can emit structured "call this function with these args" output, wired to code that actually executes it, in a loop.**

### What "tool calling" actually is under the hood
The model isn't executing code. It's trained to, when appropriate, output a structured object like:
```json
{"name": "get_weather", "arguments": {"city": "Delhi"}}
```
instead of (or alongside) natural language. LangChain standardizes this across providers so you don't hand-write provider-specific JSON schemas.

### Defining a tool in LangChain
Simplest way — the `@tool` decorator:
```python
from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    """Get the current weather for a given city."""
    return f"It's sunny in {city}."
```
- The **docstring becomes the tool description** the model sees — this is not a comment, it's part of the prompt. Write it like you're explaining the tool to someone deciding whether to use it.
- Type hints become the JSON schema for arguments automatically.
- For more control (custom schema, async, returning artifacts), use `StructuredTool.from_function()` or subclass `BaseTool`.

### Binding tools to a model
```python
model_with_tools = model.bind_tools([get_weather, search_tool])
response = model_with_tools.invoke("What's the weather in Delhi?")
response.tool_calls  # -> [{"name": "get_weather", "args": {"city": "Delhi"}, "id": "..."}]
```
Note: `bind_tools` does **not execute** the tool. It just tells the model "these are available" and lets the model *request* a call. **You** (or the agent runtime) are responsible for:
1. Reading `response.tool_calls`
2. Actually calling the Python function
3. Wrapping the result in a `ToolMessage(content=result, tool_call_id=call["id"])`
4. Appending that back into the message list and calling the model again

That 4-step loop, repeated, **is** the ReAct agent (Lesson 04). Understanding this manual loop before using `create_react_agent` (Lesson 06) will make the prebuilt helper feel obvious instead of magic.

### Tool choice / forcing
- `tool_choice="auto"` (default) — model decides whether to call a tool at all
- `tool_choice="required"` / naming a specific tool — force a call, useful in constrained pipelines
- `parallel_tool_calls` — some providers let the model request multiple tool calls in one turn (e.g., search + calculator simultaneously)

### Tool error handling
If a tool throws, don't let the exception kill the agent loop. Standard pattern: catch it, and return the **error message itself as the `ToolMessage` content**. This lets the model see "that failed because X" and self-correct on the next reasoning step — which is often more robust than you writing retry logic.

## Important Points
- Tool **description quality is a prompt-engineering problem**, not a coding problem. Vague docstrings → the model calls the wrong tool or with wrong args. This is the #1 source of agent bugs.
- Keep tool count reasonable (roughly <15-20 for most models before selection accuracy degrades) — if you have many tools, consider a retrieval step that first narrows the toolset (dynamic tool selection).
- Args should be simple, well-typed, and minimal. Avoid deeply nested objects as tool args if you can flatten them.
- `ToolMessage.tool_call_id` **must** match the `id` from the original `tool_calls` entry — mismatches are a common silent bug (model gets confused about which result maps to which call, especially with parallel calls).
- Tools that hit external APIs (Lesson 07: Tavily) need timeouts and graceful failure — an agent stuck waiting on a hung API call is a real production failure mode.

## Course Mapping
> Fill in: Section/Lecture on `@tool`, `bind_tools`, custom tool schemas.

## Research/Reference
- OpenAI function calling announcement/docs (the de facto standard other providers converged toward) — good background even if you're using a different provider.
- Anthropic tool use docs — if using Claude models in labs, the tool-calling contract is conceptually identical (name/description/schema → tool_use block → tool_result block).

## Hands-on Labs
- **Easy:** Write 2 tools (`add(a, b)`, `multiply(a, b)`), bind both to a model, ask a natural-language math question, and manually execute the single resulting tool call and print the `ToolMessage`.
- **Medium:** Write a 3-tool setup (calculator, unit converter, a fake "get_stock_price" that returns a hardcoded dict) and hand-roll the **full 4-step loop** (call model → check tool_calls → execute → append ToolMessage → call model again) with a `while` loop, terminating when the model returns no tool_calls. This is your "I understand what create_react_agent does for me" checkpoint — don't skip it.
- **Hard:** Add deliberate tool failure (e.g., unit converter raises `ValueError` for an unsupported unit) and prove the model self-corrects — i.e., on seeing the error `ToolMessage`, it either retries with corrected args or asks the user for clarification, without you writing any explicit retry/exception-handling logic outside the "return error as ToolMessage" pattern.

---
⬅ [[02-Prompts-Chains-Memory]] | ➡ [[04-ReAct-Agents-Theory-and-Papers]]
