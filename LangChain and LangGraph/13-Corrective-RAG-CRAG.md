---
tags: [langgraph, rag, corrective-rag, crag, papers]
prev: "[[12-Agentic-RAG-Fundamentals]]"
next: "[[14-Self-RAG]]"
---

# 13 — Corrective RAG (CRAG)

## Theory

### The problem CRAG solves
Even agentic RAG (Lesson 12) has a blind spot: once the retriever returns chunks, the pipeline generally *trusts* them. If the vector store's top-k results are actually irrelevant or low-quality (wrong document matched, stale data, ambiguous chunk), the generation step still confidently synthesizes an answer from bad context — a very common real-world RAG failure mode.

**Corrective RAG (Yan et al., 2024)** adds an explicit **retrieval evaluator** that grades retrieved documents before generation, and a corrective action based on that grade — instead of blindly trusting whatever the retriever returned.

### The core mechanism
1. **Retrieve** as normal (vector-store similarity search).
2. **Grade each retrieved document** — an LLM call (or lightweight classifier) scores each chunk as `Correct` / `Ambiguous` / `Incorrect` relative to the query.
3. **Branch based on the grades:**
   - **Correct** (at least one clearly relevant document) → proceed to a **knowledge refinement** step (the paper calls this "decompose-then-recompose": strip the relevant document down to key snippets, discarding noise) → generate.
   - **Incorrect** (nothing relevant found) → **discard retrieved docs entirely, fall back to web search** for fresh, relevant context → generate from that instead.
   - **Ambiguous** (mixed signal) → **combine** the refined internal knowledge *and* a web search, giving the generator both.
4. **Generate** the final answer from whichever context survived the correction step.

### Why this is a meaningfully different pattern from Lesson 12's baseline
Plain agentic RAG lets the *agent* decide whether to call the retriever again; CRAG adds a **dedicated grading step that runs on every retrieval**, independent of whether the agent "feels" it needs more info. It's a systematic quality gate, not a judgment call left entirely to the generating model (which, remember, is the same model that would otherwise hallucinate confidently from bad context in the first place — you don't want the fox guarding the henhouse without a separate grading step).

### LangGraph implementation shape
This is the canonical LangGraph tutorial pattern — a graph, not a chain, because of the grading-driven branch:
```
class CRAGState(TypedDict):
    question: str
    documents: list[str]
    grades: list[str]      # "correct" / "ambiguous" / "incorrect" per document
    web_results: str
    generation: str

def retrieve(state): ...           # vector store retrieval
def grade_documents(state): ...    # LLM call per document, or batched
def decide_next_step(state):
    if any(g == "correct" for g in state["grades"]):
        return "refine_and_generate"
    elif any(g == "ambiguous" for g in state["grades"]):
        return "web_search_and_combine"
    else:
        return "web_search_only"

def web_search(state): ...         # Tavily, replacing/supplementing bad retrieval
def refine_knowledge(state): ...   # strip retrieved docs to key snippets
def generate(state): ...

# retrieve -> grade_documents -> conditional(decide_next_step) -> {3 branches} -> generate -> END
```

## Important Points
- The **grading step is itself an LLM call per document** (or a batched call grading all of them at once) — this adds latency/cost over plain RAG, which is the price of catching bad retrievals before they poison generation.
- CRAG's fallback to web search only makes sense if your agent *has* a web search tool (Tavily, Lesson 07) wired in — without it, "Incorrect" grades have nowhere productive to fall back to besides admitting failure.
- The "knowledge refinement" (decompose-then-recompose) step is often skipped in simplified tutorial implementations — many LangGraph CRAG tutorials go straight from "Correct" grade to generation without the strip-to-snippets step. Know the full paper design, but don't feel obligated to implement every detail in a lab — note where you've simplified.
- CRAG grades **retrieval quality**; it does not grade the **final generation** for hallucination — that's Self-RAG's contribution (Lesson 14). The two are complementary, not competing.

## Course Mapping
> Fill in: relevant Udemy section, if covered.

## Research/Reference
- **Corrective Retrieval Augmented Generation** — Yan, Gu, Zhu, Ling. arXiv:2401.15884 (2024). Read: Section 3 (the retrieval evaluator + 3-way action design), Section 4 (results showing improvement over plain RAG and Self-RAG baselines across 4 datasets).
- LangGraph docs / cookbook: "Corrective RAG (CRAG)" tutorial notebook — the direct implementation reference for this lesson's architecture.

## Hands-on Labs (separate notes)
- [[13.1-Easy-Document-Grader]]
- [[13.2-Medium-CRAG-Web-Fallback]]
- [[13.3-Hard-CRAG-Full-ThreeWay-Branch]]

---
⬅ [[12-Agentic-RAG-Fundamentals]] | ➡ [[14-Self-RAG]]
