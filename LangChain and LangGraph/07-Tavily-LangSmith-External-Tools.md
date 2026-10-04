---
tags: [tavily, langsmith, tools, observability]
prev: "[[06-LangGraph-Agent-Loops-and-State]]"
next: "[[08-Hands-On-Labs]]"
---

# 07 — Tavily Search, LangSmith & Building Real Tools

## Theory

### Why not just use raw Google/Bing APIs for agent search?
Regular search APIs return links + snippets meant for humans to click through. Agents need something they can dump straight into an LLM context: clean, already-summarized, LLM-optimized results. **Tavily** is a search API purpose-built for this — it's the most common "give my agent internet access" tool in LangChain tutorials for exactly that reason.

### Tavily integration
```python
from langchain_community.tools.tavily_search import TavilySearchResults
# or, newer package: from langchain_tavily import TavilySearch

tavily_tool = TavilySearchResults(max_results=3)
```
- Needs a `TAVILY_API_KEY` (free tier available — get one at tavily.com; enough for coursework/lab use).
- Returns a list of `{url, content}` dicts — `content` is already a cleaned extract, not raw HTML, which is exactly what you want as a tool `Observation` in a ReAct loop.
- Drop it straight into `tools=[tavily_tool]` for `create_react_agent` — it's a first-class citizen, the most common "hello world" real tool in every LangGraph agent tutorial.
- Params worth knowing: `max_results`, `search_depth` ("basic" vs "advanced" — advanced costs more credits but digs deeper), `include_domains`/`exclude_domains` for scoping.

### Building your own tools against arbitrary external APIs (the general pattern)
Tavily is a template for "wrap any REST API as a tool":
```python
import requests
from langchain_core.tools import tool

@tool
def get_exchange_rate(base: str, target: str) -> str:
    """Get the current exchange rate from base currency to target currency (ISO codes, e.g. USD, INR)."""
    resp = requests.get(f"https://api.exchangerate.host/latest?base={base}&symbols={target}", timeout=5)
    resp.raise_for_status()
    data = resp.json()
    return f"1 {base} = {data['rates'][target]} {target}"
```
Checklist for any real-API tool:
1. **Always set a `timeout`** on the request — an agent that hangs on a slow API is a hung agent.
2. **Docstring describes *when* to use it**, not just what it does — helps the model pick correctly among several tools.
3. **Return a string (or simple JSON-serializable structure)**, not a raw `requests.Response` — the model needs to *read* the result as text.
4. **Handle errors by returning them as the tool's result string** (Lesson 03's pattern), not by raising uncaught — let the agent's next Thought decide what to do about a failure.
5. **Never expose write/destructive API calls as a freely-callable tool without a human-in-the-loop gate** (see Lesson 06's `interrupt_before` — this is exactly why it exists).

Other commonly used ready-made tool integrations worth knowing exist (don't need to master all, just know the landscape): `WikipediaQueryRun`, `ArxivQueryRun`, `PythonREPLTool` (sandboxed code execution — powerful and risky), `requests`-based generic HTTP tools, SQL database tools (`SQLDatabaseToolkit`).

### LangSmith — observability for agents
Once agents loop and branch, **print statements stop being enough** to debug them. LangSmith is LangChain's tracing/observability platform.

Enable it with just environment variables — no code changes needed to your chains/graphs:
```bash
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=your_key
export LANGCHAIN_PROJECT=my-react-agent-labs
```
Every `.invoke()`/`.stream()` call on any Runnable (including full LangGraph graphs) automatically logs a **trace**: every node call, every tool call with its exact input/output, every intermediate `Thought`, token counts, latency per step — viewable as a tree in the LangSmith web UI.

What you actually use it for:
- **Debugging** — see exactly which tool call had bad args, or where a loop went in an unexpected direction, instead of guessing from console prints.
- **Evaluation** — LangSmith lets you build datasets of (input, expected output) pairs and run your agent against them repeatedly to measure accuracy/regressions as you change prompts or tools.
- **Cost/latency monitoring** — per-run and aggregate token usage, useful once you care about running these agents beyond toy examples.

## Important Points
- Tavily's free tier has a monthly credit limit — budget it across labs, don't burn it all in the Easy lab loop testing.
- `search_depth="advanced"` costs more credits per call than `"basic"` — default to basic while developing, switch to advanced only when basic results are clearly insufficient.
- LangSmith tracing is **opt-in via env vars** — if a trace isn't showing up, the #1 cause is a missing/misspelled env var, not a code bug.
- A trace tree in LangSmith maps almost 1:1 onto the Thought → Action → Observation cycle from Lesson 04 — use it to *literally* read the ReAct loop your agent executed, turn by turn. This is the single best way to build intuition fast.
- Don't hardcode API keys in notebooks/scripts that might get shared — use `.env` + `python-dotenv`, standard practice across every lab from here on.

## Course Mapping
> Fill in: Section/Lecture on Tavily setup, LangSmith setup/tracing.

## Research/Reference
- Tavily docs: docs.tavily.com — API reference, credit/pricing model.
- LangSmith docs: docs.smith.langchain.com — Tracing, Evaluation, Datasets sections.
- No academic paper for this lesson — pure tooling/infrastructure.

## Hands-on Labs
- **Easy:** Get a Tavily API key, wire `TavilySearchResults` into a single-tool `create_react_agent`, ask it something time-sensitive your training data wouldn't know ("who won [recent event]"), and confirm it actually searches rather than guessing. Enable LangSmith tracing and find this run in the UI.
- **Medium:** Combine Tavily + your Lesson 03 calculator tool into one ReAct agent and give it a question requiring both ("search for the current population of Japan, then calculate what 2% of that is"). Pull up the LangSmith trace and manually verify the Thought/Action/Observation sequence matches what you'd expect from the ReAct paper's description.
- **Hard:** Build a 3-tool agent: Tavily search + your own hand-written custom API tool (pick any free public API — exchange rates, a joke API, weather, anything) + a `PythonREPLTool` for calculations too complex for a simple calculator tool. Set up a small LangSmith **evaluation dataset** of 5 test questions with expected answer substrings, and write a script that runs the agent against all 5 and reports pass/fail using LangSmith's evaluation utilities (or a simple manual substring check against the traced outputs if you don't want to set up formal eval chains yet).

---
⬅ [[06-LangGraph-Agent-Loops-and-State]] | ➡ [[08-Hands-On-Labs]]
