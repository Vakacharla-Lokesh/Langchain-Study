---
tags: [langgraph, reflection, agents]
prev: "[[09-ReWOO-Agents]]"
next: "[[11-Reflexion-Agents]]"
---

# 10 — Reflection Agents

## Theory

### The core idea
A **Reflection agent** generates an output, then has a *second pass* — often the same model in a different role, or a separate "critic" call — evaluate that output and produce feedback, which then informs a revision. Repeat until the critic is satisfied or a max-iteration cap is hit.

```
Generate → Reflect (critique) → Revise → Reflect → Revise → ... → Final
```

You've actually already built the skeleton of this: **Lesson 05's Hard lab** (draft/critique cyclic graph) *is* a reflection agent, minimal version. This lesson formalizes the pattern and extends it.

### Why reflection helps
LLMs are generally **better at judging output quality than producing perfect output on the first try** — the same asymmetry that makes "review someone else's code" easier than "write bug-free code from scratch." Reflection exploits this: instead of asking the model to be right immediately, you ask it to be right *eventually*, by giving it a structured way to catch its own mistakes.

This is a distinct pattern from ReAct/ReWOO — those are about **acting in the world via tools**; Reflection is about **improving a generated artifact through self-critique**, often with no tools involved at all (pure text generation, revised against feedback). The two are frequently combined in more advanced agents (e.g., an agent that reflects on whether its *tool usage strategy* was good, not just its final text).

### Two common architectures
1. **Single-model reflection** — same model plays both Generator and Critic, via different prompts/system messages. Cheaper, simpler, but risks the model being "too agreeable with itself" (it wrote the flawed output, so it may not spot its own blind spots).
2. **Two-model reflection** — a stronger/different model (or the same model with a very different framing, e.g., explicitly told "you are a harsh critic, not the author") critiques the generator's output. More robust at catching real flaws, at added cost.

### Implementing in LangGraph
Same shape as Lesson 05's Hard lab, formalized:
```
class State(TypedDict):
    draft: str
    critique: str
    revision_count: int

def generate(state): ...      # produce/revise draft based on critique (if any)
def reflect(state): ...       # critique the current draft, return specific feedback
def should_continue(state):
    if state["revision_count"] >= MAX or "no issues" in state["critique"].lower():
        return "end"
    return "revise"

# generate -> reflect -> conditional(should_continue) -> {revise: generate, end: END}
```
Key difference from a generic draft/critique loop: the **critique prompt matters as much as the generation prompt**. A critic that just says "looks good!" every time defeats the purpose — you want a critic prompted to actively look for specific categories of flaws (factual accuracy, structure, tone, completeness — whatever's relevant to the task).

## Important Points
- Reflection adds **real latency and cost** — every iteration is at least 2 LLM calls (generate + reflect). Always cap iterations; diminishing returns set in fast (usually 2-3 rounds captures most of the benefit).
- The critique should be **specific and actionable**, not a vague quality score — "the second paragraph lacks a citation for the population claim" drives a useful revision; "this could be better" doesn't.
- Reflection without persistent memory of *why* past attempts failed is just local hill-climbing — Lesson 11 (Reflexion) extends this pattern by adding a memory of past reflections across multiple *separate* attempts at a task, not just within one generate/critique cycle.
- Don't confuse this with RLHF or fine-tuning — reflection is a purely **inference-time, prompting-based** pattern; no weights are updated.

## Course Mapping
> Fill in: relevant Udemy section, if covered.

## Research/Reference
- **Self-Refine: Iterative Refinement with Self-Feedback** — Madaan et al., arXiv:2303.17651 (2023). The foundational "generate → feedback → refine" loop this lesson describes, evaluated across 7 diverse tasks (code, math, dialogue, etc.) showing consistent quality improvements from self-feedback alone, no additional training.
- Conceptually a precursor/sibling to Reflexion (Lesson 11) — read Self-Refine first if you want the simpler version before Reflexion's added memory layer.

## Hands-on Labs (separate notes)
- [[10.1-Easy-Reflection-Essay-Critique]]
- [[10.2-Medium-Reflection-Code-Review-Loop]]
- [[10.3-Hard-Reflection-TwoModel-Critic]]

---
⬅ [[09-ReWOO-Agents]] | ➡ [[11-Reflexion-Agents]]
