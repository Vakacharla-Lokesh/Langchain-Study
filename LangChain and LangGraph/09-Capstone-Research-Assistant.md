---
tags: [lab, capstone, portfolio]
parent: "[[08-Hands-On-Labs]]"
level: Capstone
code: CAPSTONE
---

# Capstone — Research Assistant ReAct Agent

## Aim
Build a portfolio-worthy "Research Assistant" ReAct agent combining everything from Lessons 01–07 into one coherent, production-shaped project — hand-wired `StateGraph`, checkpointed memory, a human-approval gate on risky actions, and full LangSmith observability with a saved evaluation set.

## Agent Loop Shape
Hand-built `StateGraph` ReAct loop (not the prebuilt helper — proves the wiring is understood), with `interrupt_before` on at least one tool.

## Required Components
- [ ] **Tavily** for live web search
- [ ] One custom tool relevant to your own portfolio angle — suggestions below
- [ ] Hand-built `StateGraph` (agent node + `ToolNode` + conditional edge + cycle back)
- [ ] `MemorySaver` (or `SqliteSaver` for a more real deployment) so the agent remembers context across multiple questions in one session
- [ ] `interrupt_before` on whichever tool call you'd consider "risky" — your own judgment call, document why
- [ ] Full LangSmith tracing enabled, plus at least one saved evaluation dataset (5+ questions) with pass/fail or LLM-judge scoring
- [ ] A `README.md` explaining the agent-loop diagram (Thought/Action/Observation) in your own words, citing the ReAct paper (Yao et al., arXiv:2210.03629)

## Suggested Custom Tool Ideas (pick one, or combine)
| Idea | Free API | Notes |
|---|---|---|
| GitHub repo stats lookup | GitHub REST API (`api.github.com`, no key for low-volume unauthenticated use) | Fits your GitHub-facing portfolio angle directly |
| arXiv paper search | arXiv API (`export.arxiv.org/api/query`, no key) | Nice thematic tie-in given this whole vault started from the ReAct paper |
| Weather-aware assistant | Open-Meteo (`open-meteo.com`, no key) | Simplest to wire correctly, good for a first custom tool |
| Currency/crypto assistant | Frankfurter (`api.frankfurter.app`, no key) or CoinGecko (`api.coingecko.com`, no key for basics) | Good for a finance-flavored capstone |
| Job-market lookup | Adzuna, Jooble, or similar (free tier, key required) | Directly relevant given an active job search — could double as a genuinely useful personal tool |

## Pseudocode Skeleton
```
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

tools = [tavily_tool, your_custom_tool]
model_with_tools = model.bind_tools(tools)

def call_model(state):
    return {"messages": [model_with_tools.invoke(state["messages"])]}

def should_continue(state):
    return "tools" if state["messages"][-1].tool_calls else "end"

builder = StateGraph(AgentState)
builder.add_node("agent", call_model)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", should_continue, {"tools": "tools", "end": END})
builder.add_edge("tools", "agent")

graph = builder.compile(
    checkpointer=MemorySaver(),
    interrupt_before=["tools"],   # or scope this to only the "risky" tool, see hints
)
```

## Hints & Suggestions
- If only *one* of your tools is risky, don't `interrupt_before` on every tool call — instead, branch the conditional edge so only calls to the risky tool route through an approval step, while the safe tool (e.g., search) executes freely. This is a meaningfully harder but more realistic version of Lab H2's blanket interrupt.
- Budget your Tavily free-tier credits across capstone testing — don't burn them all in one debugging session; use `search_depth="basic"` while iterating and switch to `"advanced"` only for final validation runs.
- Write the evaluation questions *before* building the full agent — designing them first forces you to think about what "correct" looks like, rather than retrofitting an eval to whatever the agent happens to output.
- Keep the README's ReAct explanation in your own words — this is the artifact you'd actually talk through in an interview, so make sure you could explain it without looking at your notes.

## GitHub References
- `langchain-ai/react-agent` — official LangGraph Studio ReAct template; a clean structural reference for organizing a capstone-scale project (`src/react_agent/graph.py`, `tools.py`, `.env.example`).
- `MuhammadAbdullah95/langgraph-cookbook` — broader agentic design patterns folder, useful if you want to extend the capstone with a second cooperating agent later.
- `Ashot72/React-Multi-Agent-Chat-with-LangGraph` — shows a full human-in-the-loop + search-agent + UI project end to end, good aspirational reference for "what this could grow into."

## Further Reading
- Yao et al., *ReAct: Synergizing Reasoning and Acting in Language Models* — arXiv:2210.03629 (cite this in your README).
- LangGraph docs: "Prebuilt ReAct Agent," "Persistence," and "Human-in-the-loop" pages — the three conceptual pillars this capstone integrates.
- LangSmith docs: "Evaluation quickstart."

---
⬅ Back to [[08-Hands-On-Labs]] full bank | 🏠 [[00-Index]]
