---
tags: [langgraph, rag, self-rag, papers]
prev: "[[13-Corrective-RAG-CRAG]]"
next: "[[15-Adaptive-RAG]]"
---

# 14 — Self-RAG

## Theory

### What Self-RAG adds beyond CRAG
CRAG (Lesson 13) grades retrieved *documents*. **Self-RAG (Asai et al., 2023)** goes further: it trains/prompts the model to reflect at **multiple points** in the pipeline using special "reflection tokens," deciding not just whether retrieved documents are good, but:
1. **Whether to retrieve at all** for this query
2. **Whether each retrieved passage is relevant**
3. **Whether the generated output is actually supported by the retrieved passages** (grounding/hallucination check)
4. **Whether the generated output is a useful, complete response to the query**

The original paper implements this via special tokens the model is fine-tuned to emit (`[Retrieve]`, `[IsRel]`, `[IsSup]`, `[IsUse]`) — but the **pattern is fully replicable via prompting alone** in a LangGraph implementation, without any fine-tuning, by making each of those four decisions an explicit graph node with its own grading prompt. This is what every LangGraph "Self-RAG" tutorial actually builds.

### The four reflection checkpoints, as LangGraph nodes
1. **Retrieval decision node** — "Does this question need external knowledge, or can it be answered directly?" (skip retrieval entirely for simple/conversational queries — saves latency and avoids irrelevant-context risk for questions that don't need it)
2. **Relevance grading node** — same idea as CRAG's document grader (Lesson 13) — is each retrieved chunk actually relevant to the question?
3. **Hallucination/groundedness grading node** — *after generation*, check: is the generated answer actually supported by the retrieved documents, or did the model add unsupported claims? If not grounded → regenerate, possibly with a stricter "only use the provided context" instruction.
4. **Answer-quality/usefulness grading node** — is the (now grounded) answer actually a good, complete response to the original question? If not → loop back, potentially retrieving more or reformulating.

### LangGraph implementation shape
```
class SelfRAGState(TypedDict):
    question: str
    documents: list[str]
    generation: str

def decide_to_retrieve(state): ...   # routes to retrieve or straight to generate
def retrieve(state): ...
def grade_relevance(state): ...      # filters documents list down to relevant ones
def generate(state): ...
def grade_hallucination(state):
    # "grounded" / "not grounded" — checks generation against documents
    ...
def grade_answer_quality(state):
    # "useful" / "not useful" — checks generation against the original question
    ...

# question -> conditional(decide_to_retrieve) -> {retrieve, generate directly}
# retrieve -> grade_relevance -> generate
# generate -> grade_hallucination -> conditional:
#     not grounded -> back to generate (regenerate)
#     grounded -> grade_answer_quality -> conditional:
#         not useful -> back to retrieve (try different query/documents)
#         useful -> END
```
Notice this has **two distinct loop-back points** — one for ungrounded generations (regenerate from the same documents), one for grounded-but-unhelpful answers (go back further, to retrieval). This is more branching complexity than CRAG's single 3-way fork, which is exactly the added sophistication Self-RAG contributes.

### Self-RAG vs. CRAG — when to reach for which
| | CRAG | Self-RAG |
|---|---|---|
| Grades | Retrieved documents only | Retrieval necessity + documents + generation grounding + generation usefulness |
| Loop-back points | 1 (retrieval quality branch) | 2 (regenerate on hallucination, re-retrieve on unhelpful answer) |
| Best for | Knowledge bases where retrieval quality is the main failure mode | Pipelines where hallucination (ungrounded generation) is a specific, measured concern worth extra checking |
| Cost | Lower (fewer grading calls) | Higher (more grading calls, more potential loop iterations) |

## Important Points
- The **hallucination-grading node is Self-RAG's standout contribution** relative to everything covered so far — none of Lessons 04/09/12/13 explicitly check "is the final answer actually supported by evidence," they focus on retrieval or action quality, not generation-vs-evidence grounding.
- Always cap total loop iterations (both loop-back points combined) — with two separate conditional retry paths, an unlucky combination could otherwise cycle for a while. Reuse Lesson 04's max-iteration discipline.
- The **prompted (non-fine-tuned) version of Self-RAG**, which is what you'll build in LangGraph, is an approximation of the paper's trained-token approach — it's a legitimate, widely-used simplification (this is exactly what the LangGraph cookbook's own Self-RAG tutorial does), but know that the original research result used a fine-tuned model with dedicated reflection tokens, which is a stronger (and much more expensive to set up) version of the same idea.
- Self-RAG's "grounded but not useful" branch is easy to skip in a simplified build — many tutorial implementations only implement the hallucination check and treat "grounded" as good enough. Decide deliberately whether your lab implements both checkpoints or just the hallucination one, and note which you built.

## Course Mapping
> Fill in: relevant Udemy section, if covered.

## Research/Reference
- **Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection** — Asai, Wu, Wang, Sil, Hajishirzi. arXiv:2310.11511 (2023). Read: Section 2 (the 4 reflection token types), Section 4 (results on open-domain QA and long-form generation vs. plain RAG baselines).
- LangGraph docs / cookbook: "Self-RAG" tutorial notebook — the direct prompted (non-fine-tuned) implementation reference this lesson is based on.

## Hands-on Labs (separate notes)
- [[14.1-Easy-Retrieval-Decision-Gate]]
- [[14.2-Medium-Hallucination-Grader]]
- [[14.3-Hard-Full-Self-RAG-Graph]]

---
⬅ [[13-Corrective-RAG-CRAG]] | ➡ [[15-Adaptive-RAG]]
