---
tags: [langgraph, rag, adaptive-rag, papers]
prev: "[[14-Self-RAG]]"
next: "[[00-Index]]"
---

# 15 — Adaptive RAG

## Theory

### The insight Adaptive RAG is built on
Not every query needs the same amount of machinery. **"What is the capital of France?"** doesn't need retrieval at all — the model just knows it. **"When did the person who captured Malakoff arrive in the region where Philipsburg is located?"** is a genuine multi-hop question that needs iterative, agentic retrieval (Lesson 12's pattern, possibly with CRAG/Self-RAG's grading layered in). Running the expensive multi-step agentic pipeline on the first question wastes latency and money; running the cheap direct-answer path on the second produces a wrong or incomplete answer.

**Adaptive RAG (Jeong et al., 2024)** adds a **query complexity classifier** at the very front of the pipeline that routes each incoming question to the cheapest strategy that's actually sufficient for it, rather than running every query through the same fixed pipeline.

### The three-way (or more) routing
A typical Adaptive RAG router classifies each query into a tier and routes accordingly:
1. **No retrieval needed** — simple factual/general-knowledge questions the model can answer directly. Route straight to generation, skip retrieval entirely.
2. **Single-step RAG** — the question needs external/internal knowledge, but a single retrieve-then-generate pass is sufficient (no need for iteration or multi-hop reasoning).
3. **Multi-step / iterative RAG** — genuinely complex, multi-hop, or ambiguous questions that need the full agentic RAG treatment — potentially combined with CRAG's document grading (Lesson 13) and/or Self-RAG's hallucination checking (Lesson 14) for maximum reliability on the hardest queries.

### LangGraph implementation shape
```
class AdaptiveRAGState(TypedDict):
    question: str
    route: str
    documents: list[str]
    generation: str

def route_question(state):
    # LLM call: classify as "no_retrieval" / "single_step" / "multi_step"
    ...

def generate_direct(state): ...        # no retrieval, straight answer
def single_step_rag(state): ...        # retrieve once, generate
def multi_step_rag_subgraph(state):    # invokes the Lesson 12/13/14 agentic/CRAG/Self-RAG graph
    ...

builder.add_conditional_edges("route_question", lambda s: s["route"], {
    "no_retrieval": "generate_direct",
    "single_step": "single_step_rag",
    "multi_step": "multi_step_rag_subgraph",
})
```
**Important architectural note:** the "multi_step" branch is often not a single node but an entire **sub-graph** — this is where you'd literally embed your Lesson 13 (CRAG) or Lesson 14 (Self-RAG) graph as a node within this larger Adaptive RAG graph. LangGraph supports compiled graphs as nodes inside other graphs, which is exactly the mechanism for this kind of composition — Adaptive RAG is best understood as **the outermost routing layer that decides which of the earlier lessons' architectures to invoke**, not a wholly separate technique competing with them.

### How to build the router itself
The router is typically a small structured-output classification call:
```python
class RouteQuery(BaseModel):
    datasource: Literal["no_retrieval", "single_step", "multi_step"]

router = model.with_structured_output(RouteQuery)
```
Few-shot examples in the router's prompt (Lesson 02's `FewShotPromptTemplate` pattern) meaningfully improve routing accuracy — this is a classification task like any other, and classification quality is highly sensitive to example quality.

## Important Points
- Adaptive RAG is the **capstone pattern of the RAG-variant lessons (12-15)** — it doesn't replace CRAG or Self-RAG, it decides *when* to invoke them (or skip them entirely) per query. Think of Lessons 12-14 as tools in Adaptive RAG's toolbox, selected by the router.
- Router misclassification is the main failure mode — a genuinely complex question misrouted to "no_retrieval" produces a confidently wrong answer with no retrieval to catch it. If you notice this happening often in testing, it usually means the router's few-shot examples need to cover more edge cases, not that the downstream RAG logic is broken.
- This pattern generalizes well beyond RAG specifically — "classify query complexity, route to the cheapest sufficient pipeline" is a broadly useful cost/latency-optimization pattern for any agent system with multiple possible execution paths of different expense.
- Building this well requires you to be comfortable with everything in Lessons 05 (conditional edges), 12 (agentic RAG), 13 (CRAG), and 14 (Self-RAG) — it's intentionally the last lesson in this sequence for that reason.

## Course Mapping
> Fill in: relevant Udemy section, if covered.

## Research/Reference
- **Adaptive-RAG: Learning to Adapt Retrieval-Augmented Large Language Models through Question Complexity** — Jeong, Baek, Cho, Hwang, Park. arXiv:2403.14403 (2024). Read: Section 3 (the complexity classifier design and training), Section 4 (results showing efficiency gains from routing simple queries away from expensive multi-step pipelines, without sacrificing accuracy on genuinely complex ones).
- LangGraph docs / cookbook: "Adaptive RAG" tutorial notebook — the direct implementation reference, which itself builds on the same repo's CRAG and Self-RAG notebooks (Lessons 13/14).

## Hands-on Labs (separate notes)
- [[15.1-Easy-Query-Complexity-Router]]
- [[15.2-Medium-Adaptive-Three-Way-Routing]]
- [[15.3-Hard-Adaptive-RAG-With-CRAG-SelfRAG-Subgraphs]]

---
⬅ [[14-Self-RAG]] | 🏠 [[00-Index]]
