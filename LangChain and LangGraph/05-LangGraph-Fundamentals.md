---
tags: [langgraph, state, graphs]
prev: "[[04-ReAct-Agents-Theory-and-Papers]]"
next: "[[06-LangGraph-Agent-Loops-and-State]]"
---

# 05 — LangGraph Fundamentals

## Theory

### Why LangGraph exists (bridge from Lesson 04)
LCEL (Lesson 01) composes Runnables into a **DAG** — data flows one direction, no cycles, no runtime branching by the LLM itself. ReAct agents *need* cycles ("call model → maybe call tool → call model again") and conditional branching ("if the model wants a tool, go execute it; if not, end"). LangGraph is LangChain's answer: a low-level orchestration layer built around an explicit **graph of nodes and edges over a shared State object**, which naturally supports loops, branches, and persistence.

### Core building blocks

**1. State**
A typed schema (usually a `TypedDict` or Pydantic model) representing everything the graph carries between steps.
```python
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
```
- `Annotated[list, add_messages]` is a **reducer** — it tells LangGraph *how* to merge a node's return value into the existing state, rather than overwriting it. `add_messages` specifically appends new messages (and handles de-duping by message ID). Without a reducer, returning `{"messages": [...]}` from a node would *replace* the whole list, not append — this trips people up constantly.

**2. Nodes**
Plain Python functions (or Runnables) that take the current State and return a partial State update:
```python
def call_model(state: AgentState):
    response = model.invoke(state["messages"])
    return {"messages": [response]}
```

**3. Edges**
Connect nodes. Two kinds:
- **Normal edges** — always go from A to B: `graph.add_edge("node_a", "node_b")`
- **Conditional edges** — a function inspects state and returns which node to go to next: `graph.add_conditional_edges("call_model", should_continue, {"continue": "tools", "end": END})`. This is exactly how the ReAct loop's "did the model request a tool, or is it done?" branch gets implemented.

**4. `START` / `END`**
Special sentinel nodes marking entry and exit points of the graph.

**5. Compiling**
`graph.compile()` turns the declarative graph definition into a runnable object (itself a `Runnable`, so `.invoke()`/`.stream()` work the same way as Lesson 01).

### StateGraph vs. LCEL — when to use which
| | LCEL | LangGraph |
|---|---|---|
| Control flow | Fixed, linear/parallel | Dynamic, can branch & loop |
| Who decides the path | You, at build time | The graph (often driven by model output) at runtime |
| Best for | RAG pipelines, formatting/extraction chains, anything with no looping | Agents, multi-step workflows, anything needing memory/checkpointing across turns |
| Composability | You can embed an LCEL chain **inside** a LangGraph node | N/A (LangGraph is the "outer" layer usually) |

**Practical rule of thumb:** if you can draw the logic as a straight line (or a fork that never rejoins/loops), use LCEL. The moment you need "go back and do this again based on a decision," reach for LangGraph.

### Visualizing
Every compiled graph can render itself: `graph.get_graph().draw_mermaid_png()` or `.print_ascii()`. Use this constantly while debugging — a graph that's wired wrong is much easier to spot visually than by reading node code.

## Important Points
- State updates are **partial and merged via reducers**, not full replacements, by default for anything you `Annotated` with a reducer — but plain (non-annotated) fields in State *are* overwritten by whatever a node returns for that key. Know which fields in your State use a reducer and which don't.
- Nodes should be small and single-purpose (one node = one LLM call, or one tool execution step, or one decision point) — resist cramming multiple responsibilities into one node; it defeats the point of the graph being inspectable/debuggable.
- `add_conditional_edges` routing functions must return a value that exactly matches a key in the mapping dict you pass — a common bug is returning a string that doesn't match any key, which raises at runtime, not at graph-build time.
- LangGraph graphs are just Python — no magic DSL beyond the `add_node`/`add_edge` calls. This makes them easy to unit test node-by-node before wiring the full graph.

## Course Mapping
> Fill in: Section/Lecture introducing StateGraph, nodes/edges, `add_conditional_edges`.

## Research/Reference
- LangGraph conceptual docs: "Low Level Concepts" — State, Nodes, Edges, Reducers.
- No academic paper here — this is a systems/framework design, not a research contribution. (Its *design philosophy* is influenced by actor-model / graph-of-computation ideas common in workflow engines, worth knowing conceptually but not required reading.)

## Hands-on Labs
- **Easy:** Build a 3-node linear graph (no branching) that takes a topic string, generates an outline (node 1), expands it into a paragraph (node 2), and shortens it back to a tweet (node 3). Print `graph.get_graph().print_ascii()` before running it.
- **Medium:** Build a graph with a **conditional edge**: a node classifies incoming text as "question" or "complaint," and routes to a different response-generating node depending on the classification. Confirm both branches by testing with one input of each type.
- **Hard:** Build a graph with an actual **cycle**: a "generate draft" node → "critique draft" node (an LLM call that either says "good enough" or gives specific feedback) → conditional edge that loops back to "generate draft" (now including the critique in context) if not good enough, or goes to `END` if it is. Cap it at 4 iterations to avoid infinite loops, and print how many iterations it actually took to converge.

---
⬅ [[04-ReAct-Agents-Theory-and-Papers]] | ➡ [[06-LangGraph-Agent-Loops-and-State]]
