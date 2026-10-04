---
tags: [moc, langchain, langgraph, index]
status: in-progress
started: 2026-09-22
---

# 🗂️ LangChain + LangGraph — Master Index

> Context: Learning this for **project training** (not a side hobby). Focus: **ReAct agents**, tool calling, and the LangGraph agentic loop, with a Udemy course as the primary source + supplementary papers.

## How this vault is organized
Each lesson note follows the same skeleton so you can scan fast:
- **Theory** — concept explained from first principles
- **Important Points** — the stuff that actually gets asked/used/breaks in practice
- **Course Mapping** — where this sits in the Udemy course structure (fill in section/lecture numbers as you go)
- **Research/Reference** — papers or docs backing the concept
- **Hands-on Labs** — Easy / Medium / Hard, each with agent-loop spec + hints (full lab bank lives in `08-Hands-On-Labs.md`, cross-linked per lesson)

## 📚 Lesson Order

| # | Note | Core Topic |
|---|------|------------|
| 01 | [[01-LangChain-Fundamentals]] | LLM wrappers, runnables, LCEL, output parsers |
| 02 | [[02-Prompts-Chains-Memory]] | PromptTemplates, chains, memory strategies |
| 03 | [[03-Tool-Calling-and-Function-Calling]] | Tool schemas, `@tool` decorator, binding tools to models |
| 04 | [[04-ReAct-Agents-Theory-and-Papers]] | ReAct pattern, Reason+Act loop, the ReAct paper |
| 05 | [[05-LangGraph-Fundamentals]] | Graphs, nodes, edges, State, StateGraph vs LCEL |
| 06 | [[06-LangGraph-Agent-Loops-and-State]] | `create_react_agent`, conditional edges, checkpointing, cycles |
| 07 | [[07-Tavily-LangSmith-External-Tools]] | Tavily search tool, LangSmith tracing/eval, building custom tools |
| 08 | [[08-Hands-On-Labs]] | Full lab bank (Easy/Medium/Hard) across Lessons 01-07 |
| 09 | [[09-ReWOO-Agents]] | Reasoning WithOut Observation — Planner/Worker/Solver, decoupled reasoning |
| 10 | [[10-Reflection-Agents]] | Generate → critique → revise loop, Self-Refine pattern |
| 11 | [[11-Reflexion-Agents]] | Verbal reinforcement learning — reflection memory across attempts |
| 12 | [[12-Agentic-RAG-Fundamentals]] | Retriever as a tool inside a ReAct loop |
| 13 | [[13-Corrective-RAG-CRAG]] | Grading retrieved documents, web-search fallback |
| 14 | [[14-Self-RAG]] | Retrieval-necessity, relevance, groundedness & usefulness self-grading |
| 15 | [[15-Adaptive-RAG]] | Query-complexity routing across no-retrieval / single-step / multi-step RAG |

### 🧪 Hands-on labs for Lessons 09-15 (separate notes, `labs/` folder)
| Lesson | Easy | Medium | Hard |
|---|---|---|---|
| 09 ReWOO | [[09.1-Easy-ReWOO-Basic-Planner]] | [[09.2-Medium-ReWOO-Multi-Step-Worker]] | [[09.3-Hard-ReWOO-vs-ReAct-Benchmark]] |
| 10 Reflection | [[10.1-Easy-Reflection-Essay-Critique]] | [[10.2-Medium-Reflection-Code-Review-Loop]] | [[10.3-Hard-Reflection-TwoModel-Critic]] |
| 11 Reflexion | [[11.1-Easy-Reflexion-Memory-Buffer]] | [[11.2-Medium-Reflexion-QA-Retry-Loop]] | [[11.3-Hard-Reflexion-Coding-Agent]] |
| 12 Agentic RAG | [[12.1-Easy-Retriever-As-Tool]] | [[12.2-Medium-Multi-Round-Agentic-RAG]] | [[12.3-Hard-Agentic-RAG-With-Fallback]] |
| 13 Corrective RAG | [[13.1-Easy-Document-Grader]] | [[13.2-Medium-CRAG-Web-Fallback]] | [[13.3-Hard-CRAG-Full-ThreeWay-Branch]] |
| 14 Self-RAG | [[14.1-Easy-Retrieval-Decision-Gate]] | [[14.2-Medium-Hallucination-Grader]] | [[14.3-Hard-Full-Self-RAG-Graph]] |
| 15 Adaptive RAG | [[15.1-Easy-Query-Complexity-Router]] | [[15.2-Medium-Adaptive-Three-Way-Routing]] | [[15.3-Hard-Adaptive-RAG-With-CRAG-SelfRAG-Subgraphs]] |

## 🎯 Learning Goals (fill in / edit as needed)
- [ ] Understand LCEL well enough to compose chains without copy-pasting
- [ ] Build a tool-calling agent from scratch (no prebuilt helper) at least once
- [ ] Understand *why* ReAct interleaves reasoning traces with actions (not just *how*)
- [ ] Port the ReAct agent from LangChain's AgentExecutor style to LangGraph's `StateGraph`
- [ ] Get one agent fully traced in LangSmith and read a trace end-to-end
- [ ] Ship one "hard" lab project usable as a portfolio artifact

## 🔑 Core Vocabulary (quick lookup — expand as terms come up)
| Term | One-line definition |
|---|---|
| Runnable | LangChain's universal interface (`.invoke`, `.batch`, `.stream`) any component implements |
| LCEL | LangChain Expression Language — pipe (`\|`) syntax to compose Runnables |
| Agent | LLM that decides *which action to take next*, in a loop, using tool outputs as new context |
| Tool | A function exposed to the LLM with a name, description, and typed args schema |
| ReAct | Prompting/agent pattern: **Reason** (thought) → **Act** (tool call) → **Observe** (tool result) → repeat |
| StateGraph | LangGraph's core abstraction — a graph of nodes that read/write a shared State object |
| Checkpointer | LangGraph's persistence layer for state across steps/threads (enables memory, human-in-loop) |
| AgentExecutor | Legacy LangChain agent runtime (pre-LangGraph) — good to know, not where the ecosystem is headed |
| ReWOO | Reasoning WithOut Observation — plans all tool calls upfront (Planner), executes them (Worker), synthesizes at the end (Solver) |
| Reflection | Generate → critique → revise loop; model improves its own output via self-feedback, no tools required |
| Reflexion | Reflection across multiple separate task attempts, with a persistent memory of past lessons learned ("verbal reinforcement learning") |
| Agentic RAG | Retrieval exposed as a callable tool inside a ReAct loop, instead of a fixed retrieve-then-generate pipeline |
| CRAG | Corrective RAG — grades retrieved documents, falls back to web search when retrieval is poor |
| Self-RAG | Self-grades retrieval necessity, document relevance, generation groundedness, and answer usefulness |
| Adaptive RAG | Routes each query to the cheapest sufficient strategy based on a query-complexity classifier |

## 🔗 External Resources (canonical, not tutorial fluff)
- LangChain Python docs: https://python.langchain.com/
- LangGraph docs: https://langchain-ai.github.io/langgraph/
- LangSmith docs: https://docs.smith.langchain.com/
- Tavily API docs: https://docs.tavily.com/
- ReAct paper (Yao et al., 2022): *ReAct: Synergizing Reasoning and Acting in Language Models* — arXiv:2210.03629
- ReWOO paper (Xu et al., 2023): *ReWOO: Decoupling Reasoning from Observations* — arXiv:2305.18323 | reference repo: `billxbf/ReWOO`
- Self-Refine paper (Madaan et al., 2023): arXiv:2303.17651 (Reflection pattern)
- Reflexion paper (Shinn et al., 2023): arXiv:2303.11366 | reference repo: `noahshinn/reflexion`
- Corrective RAG paper (Yan et al., 2024): arXiv:2401.15884
- Self-RAG paper (Asai et al., 2023): arXiv:2310.11511
- Adaptive-RAG paper (Jeong et al., 2024): arXiv:2403.14403
- LangGraph official ReAct template: `langchain-ai/react-agent` | Agentic design patterns: `MuhammadAbdullah95/langgraph-cookbook`

## 📝 Running Log
> Append a one-liner per study session. Keeps you honest about actual hours.

- 2026-09-22 — Vault scaffolded. Starting Lesson 01.
