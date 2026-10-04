---
tags: [langgraph, rag, agentic-rag]
prev: "[[11-Reflexion-Agents]]"
next: "[[13-Corrective-RAG-CRAG]]"
---

# 12 — Agentic RAG (Fundamentals)

## Theory

### What "agentic" adds to plain RAG
Classic RAG is a fixed pipeline: **embed query → retrieve top-k chunks → stuff into prompt → generate answer.** It's an LCEL-shaped chain (Lesson 01) — no decisions, no branching, one retrieval pass no matter what.

**Agentic RAG** turns retrieval itself into a *tool* the agent can decide to call, potentially multiple times, with reformulated queries, alongside other tools — instead of a hardcoded first step. The retriever stops being "step 1 of the pipeline" and becomes "one option the model can reach for, when it judges that's the right move." This is a direct application of everything from Lessons 03/04: wrap your vector-store retriever as a `@tool`, hand it to a ReAct agent alongside (optionally) other tools like Tavily.

### Why this matters over plain RAG
Plain RAG fails silently in a few common ways agentic RAG can address:
- **Query mismatch** — the user's literal question is a poor embedding-search query (too vague, too colloquial). An agent can reformulate before retrieving.
- **Single-shot retrieval isn't enough** — some questions need multiple retrieval rounds (retrieve → realize you need a follow-up fact → retrieve again), which is just the ReAct loop applied to a retrieval tool instead of a generic search tool.
- **No fallback when the knowledge base doesn't have the answer** — plain RAG will confidently generate from irrelevant retrieved chunks. An agent can recognize "nothing relevant came back" and either say so or fall back to a different tool (e.g., web search).
- **No self-correction** — this is where the RAG-variant lessons that follow (13-15) come in: Corrective RAG, Self-RAG, and Adaptive RAG are all specific, named recipes for grading and correcting retrieval quality, layered on top of this agentic foundation.

### Minimal architecture
```python
retriever_tool = create_retriever_tool(
    vectorstore.as_retriever(),
    name="search_knowledge_base",
    description="Search internal documents about <your domain>. Use this for questions about <topic scope>."
)

agent = create_react_agent(model, tools=[retriever_tool, tavily_tool])
```
That's it structurally — the "agentic" part is entirely in how the retriever is exposed (as a tool with a good description, per Lesson 03's rules) rather than hardcoded into a chain. Everything from Lessons 04-06 (ReAct loop, LangGraph cycles, checkpointing) applies unchanged.

### Where this sits relative to the RAG-variant lessons ahead
| Lesson | Adds |
|---|---|
| 12 (this one) | Retrieval as a callable tool inside a ReAct loop — the baseline |
| 13 — Corrective RAG | Grades retrieved documents for relevance; triggers web search fallback if retrieval is bad |
| 14 — Self-RAG | Model decides *whether to retrieve at all* per query, and self-grades both retrieval relevance and its own generation for hallucination/support |
| 15 — Adaptive RAG | Routes each incoming query to the cheapest sufficient strategy (no retrieval / single-shot RAG / iterative agentic RAG) based on estimated query complexity |

Read these in order — each adds one more layer of self-correction/routing sophistication on top of this lesson's baseline.

## Important Points
- `create_retriever_tool` (from `langchain.tools.retriever`) is the standard LangChain helper that wraps any retriever into a properly-schemed tool — use it instead of hand-writing the wrapper.
- The retriever tool's **description is doing the same "which tool should the model pick" job** as any other tool description (Lesson 03) — be specific about domain/scope so the agent doesn't call it for out-of-scope questions.
- Chunking/embedding strategy (chunk size, overlap, embedding model choice) still matters exactly as much as in plain RAG — agentic RAG fixes *when and how often* retrieval happens, not the retrieval quality itself. That's what Lesson 13's document grading step addresses.
- Don't reach for full agentic RAG if plain single-shot RAG already answers your use case well — the added LLM calls (deciding whether/when to retrieve, potentially retrieving multiple times) cost real latency and money. Lesson 15 (Adaptive RAG) is literally the pattern for deciding when the extra complexity is worth it.

## Course Mapping
> Fill in: relevant Udemy section, if covered.

## Research/Reference
- No single foundational paper for "agentic RAG" as a named pattern — it's the natural combination of RAG (Lewis et al., 2020, *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*, arXiv:2005.11401) with the ReAct agent pattern (Lesson 04). Worth skimming the original RAG paper's abstract for historical grounding even though the implementation has moved on significantly.
- LangGraph docs: "Agentic RAG" tutorial — the direct implementation reference this lesson is based on.

## Hands-on Labs (separate notes)
- [[12.1-Easy-Retriever-As-Tool]]
- [[12.2-Medium-Multi-Round-Agentic-RAG]]
- [[12.3-Hard-Agentic-RAG-With-Fallback]]

---
⬅ [[11-Reflexion-Agents]] | ➡ [[13-Corrective-RAG-CRAG]]
