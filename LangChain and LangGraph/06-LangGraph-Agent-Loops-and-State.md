---
tags: [langgraph, react-agent, checkpointing, core-focus]
prev: "[[05-LangGraph-Fundamentals]]"
next: "[[07-Tavily-LangSmith-External-Tools]]"
---

# 06 — LangGraph Agent Loops & State (ReAct, implemented)
> ⭐ This is where Lesson 04's theory becomes running code.

## Theory

### The ReAct loop as a 2-node cyclic graph
The canonical LangGraph ReAct agent is (surprisingly) just two nodes and one conditional edge:

```
START → agent(call the model) → [conditional] → tools(execute tool calls) → agent → ... → END
```

- **`agent` node** — calls `model_with_tools.invoke(state["messages"])`, appends the `AIMessage` (which may contain `tool_calls`) to state.
- **`tools` node** — LangGraph ships a prebuilt `ToolNode(tools_list)` that inspects the last message's `tool_calls`, executes each matching Python tool function, and appends the resulting `ToolMessage`(s) back into state. You rarely need to hand-write this node.
- **Conditional edge (`should_continue`)** — checks if the last `AIMessage` has `tool_calls`. If yes → route to `tools`. If no (model gave a final answer) → route to `END`.
- After `tools` runs, there's a plain edge back to `agent` — **this is the cycle** that makes it a loop, not a one-shot chain.

### The prebuilt shortcut
```python
from langgraph.prebuilt import create_react_agent
agent = create_react_agent(model, tools=[search_tool, calculator_tool])
```
This constructs *exactly* the graph above for you. **Only reach for this after you've built the loop manually at least once** (Lesson 03 Medium lab did the non-graph version; do the graph version by hand too before using this) — otherwise you're memorizing an API call instead of understanding what it does.

### Checkpointing — turning "one task" into "an ongoing agent with memory"
By default a compiled graph is stateless between `.invoke()` calls — every call starts fresh. A **checkpointer** persists State after every node execution, keyed by a `thread_id`:

```python
from langgraph.checkpoint.memory import MemorySaver
checkpointer = MemorySaver()   # in-memory; swap for SqliteSaver/PostgresSaver in production
graph = builder.compile(checkpointer=checkpointer)

graph.invoke({"messages": [...]}, config={"configurable": {"thread_id": "user-123"}})
```
Every subsequent `.invoke()` with the same `thread_id` **resumes from the saved state** — this is how you get multi-turn conversational memory "for free" once you're using LangGraph, replacing the manual memory strategies from Lesson 02.

Checkpointing also unlocks:
- **Time travel** — replay/inspect state at any past checkpoint (`graph.get_state_history(config)`)
- **Human-in-the-loop** — `interrupt_before=["tools"]` pauses the graph right before executing a tool, letting a human approve/edit/reject the tool call before it runs. Critical pattern for any agent that can take real-world side-effecting actions (sending emails, making purchases, etc.)

### State schema for a real ReAct agent
Beyond `messages`, real agents often extend State with task-specific fields, e.g.:
```python
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    iteration_count: int
    max_iterations: int
```
and have the conditional edge also check `iteration_count >= max_iterations` to force termination — the concrete implementation of the "always cap your loop" rule from Lesson 04.

### Streaming an agent's steps
`graph.stream(input, config, stream_mode="values")` yields the full state after each node — this is how you'd build a UI that shows "Thinking... → Calling search tool... → Reading results... → Answering" live, instead of waiting for the whole loop to finish.

## Important Points
- `ToolNode` expects tools defined the Lesson-03 way (`@tool` or `StructuredTool`) — it introspects their schema to match `tool_calls` by name.
- `thread_id` is *your* application's concept of "a conversation" or "a session" — nothing in LangGraph assigns it automatically; you generate/manage these IDs (e.g., one per user session, one per support ticket).
- `MemorySaver` is for development only — it's wiped when the process restarts. Production needs `SqliteSaver`, `PostgresSaver`, or a custom checkpointer backed by real storage.
- `interrupt_before` / `interrupt_after` are how you implement approval gates — don't build a custom "ask user y/n" hack outside the graph when this exists natively.
- Recursion limit: LangGraph has a default max step count (`recursion_limit`, default 25) as a safety net independent of your own iteration-count field — know it exists so a runaway loop fails with a clear error instead of hanging forever.

## Course Mapping
> Fill in: Section/Lecture on `create_react_agent`, checkpointers, `interrupt_before`.

## Research/Reference
- LangGraph docs: "Agentic Concepts" and "Persistence" pages — checkpointer API, `thread_id` semantics.
- Conceptually still grounded in the ReAct paper (Lesson 04) — this lesson is "same algorithm, production-grade runtime."

## Hands-on Labs
- **Easy:** Take the Lesson 05 Hard lab's cyclic graph (draft/critique loop) and add a `MemorySaver` checkpointer with a `thread_id`. Run it, then run `graph.get_state_history(config)` afterward and print how many checkpoints were saved.
- **Medium:** Build a full ReAct agent **by hand** (not using `create_react_agent`) with a 2-tool setup from Lesson 04's Medium lab, wired as a proper `StateGraph` with `agent` node, `ToolNode`, and a conditional edge. Then rebuild the *identical* agent using `create_react_agent` in 3 lines and diff the behavior on the same 5 test questions — confirm outputs match.
- **Hard:** Build a ReAct agent with a tool that has a real side effect (e.g., a fake `send_email(to, subject, body)` tool that just prints "EMAIL SENT" — pretend it's dangerous). Add `interrupt_before=["tools"]` so the graph pauses before calling any tool, print the pending tool call for a human to review, accept manual input (`approve`/`reject`/`edit args`), and resume the graph accordingly using `graph.update_state()` + a subsequent `.invoke(None, config)`.

---
⬅ [[05-LangGraph-Fundamentals]] | ➡ [[07-Tavily-LangSmith-External-Tools]]
