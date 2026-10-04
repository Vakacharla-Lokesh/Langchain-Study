---
tags: [langgraph, reflexion, agents, papers]
prev: "[[10-Reflection-Agents]]"
next: "[[12-Agentic-RAG-Fundamentals]]"
---

# 11 — Reflexion Agents

## Theory

### How this differs from plain Reflection (Lesson 10)
Reflection (Lesson 10) critiques and revises a **single artifact within one continuous session** — draft, critique, revise, done. **Reflexion (Shinn et al., 2023)** operates across **multiple separate attempts at a task**, using natural-language self-reflection as a substitute for gradient-based learning: after a full attempt fails (or under-performs), the agent verbally reflects on *why*, stores that reflection in an episodic memory, and uses it on the *next* attempt.

This is the paper this vault already flagged as required-but-optional reading back in Lesson 04 — now it's the main event.

### The three components (paper's architecture)
1. **Actor** — the policy generating actions/text, conditioned on the task, its own trajectory so far, and any past reflections retrieved from memory. This can literally be a ReAct agent (Lesson 04) — Reflexion is designed to wrap around an existing actor, not replace it.
2. **Evaluator** — scores the outcome of a completed trajectory (e.g., did the agent solve the coding problem? Did the test suite pass? Was the QA answer correct?). Can be a heuristic (unit test pass/fail), an environment-provided reward, or another LLM call.
3. **Self-Reflection model** — given the trajectory and the Evaluator's (often sparse — "failed") signal, generates a specific, actionable verbal reflection: *"I looked up the wrong entity because I didn't verify the search result matched the question's timeframe; next time, cross-check dates before using a search result."* This reflection is stored in an episodic memory buffer.

### The loop across attempts
```
Attempt 1: Actor tries task → Evaluator scores it → if failed: Self-Reflection generates a lesson → store in memory
Attempt 2: Actor tries again, now with memory of Attempt 1's reflection in its context → Evaluator scores it → reflect if still failing → store
... repeat up to N attempts or until success
```
Crucially, **this is not fine-tuning** — nothing about the model's weights changes. The "learning" is entirely in the growing natural-language memory buffer that gets fed back into the Actor's prompt on each subsequent attempt. This is what the paper means by "verbal reinforcement learning."

### Reported results
On HotpotQA (multi-hop QA, same benchmark ReAct/ReWOO were tested on) and on coding benchmarks (HumanEval), Reflexion agents showed significant relative improvement in success rate across attempts compared to agents with no reflection memory — the improvement curve specifically comes from the accumulation of specific, task-relevant lessons across attempts, not from randomness/retrying alone (the paper compares against naive retry baselines to isolate this).

### Implementing in LangGraph
Reflexion needs state that **persists across what look like separate "episodes"** — this is exactly what a checkpointer + `thread_id` (Lesson 06) gives you, used slightly differently: instead of one long conversation, you're running repeated bounded attempts, each seeded with the accumulated reflection memory.
```
class ReflexionState(TypedDict):
    task: str
    trajectory: Annotated[list, add_messages]     # current attempt's ReAct-style trace
    reflections: list[str]                          # accumulated lessons across attempts
    attempt_number: int
    success: bool

def actor_node(state): ...      # ReAct-style agent, prompt includes state["reflections"]
def evaluator_node(state): ...  # scores the completed trajectory, sets state["success"]
def reflect_node(state): ...    # if not success: generate a new reflection, append to state["reflections"]

def should_retry(state):
    if state["success"] or state["attempt_number"] >= MAX_ATTEMPTS:
        return "end"
    return "retry"

# actor -> evaluator -> conditional(should_retry) -> {retry: reflect -> actor, end: END}
```

## Important Points
- Reflexion assumes you have **some way to evaluate success** — a unit test, a ground-truth answer, an environment signal, or at minimum an LLM-as-judge. Without a real evaluator, the reflections have nothing grounded to learn from and the pattern degrades toward Lesson 10's plain reflection.
- The reflection memory should stay **concise and specific** across attempts — dumping the entire failed trajectory into the next attempt's prompt defeats the purpose (that's just more context, not a distilled lesson); the Self-Reflection step's whole job is compression into an actionable insight.
- Reflexion is expensive: multiple full attempts, each potentially a multi-step ReAct trajectory, plus evaluation and reflection calls. Reserve it for tasks where getting it right matters more than getting it fast/cheap (e.g., a coding agent that gets several tries against a real test suite) — for most simple queries, this is overkill.
- Relation to the field: Reflexion is one of the most-cited "agent improves via verbal self-critique across attempts" papers and is a common building block cited by later multi-agent and coding-agent systems — recognizing the pattern by name is useful well beyond this specific implementation.

## Course Mapping
> Fill in: relevant Udemy section, if covered.

## Research/Reference
- **Reflexion: Language Agents with Verbal Reinforcement Learning** — Shinn, Cassano, Berman, Gopinath, Narasimhan, Yao. arXiv:2303.11366 (2023). Read: Section 3 (Actor/Evaluator/Self-Reflection architecture), the HotpotQA and HumanEval results sections.
- Builds directly on ReAct (Lesson 04) and Self-Refine (Lesson 10) — read those first if you haven't, the paper assumes familiarity with both.

## Hands-on Labs (separate notes)
- [[11.1-Easy-Reflexion-Memory-Buffer]]
- [[11.2-Medium-Reflexion-QA-Retry-Loop]]
- [[11.3-Hard-Reflexion-Coding-Agent]]

---
⬅ [[10-Reflection-Agents]] | ➡ [[12-Agentic-RAG-Fundamentals]]
