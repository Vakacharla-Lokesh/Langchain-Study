---
tags: [langgraph, rewoo, agents, papers]
prev: "[[08-Hands-On-Labs]]"
next: "[[10-Reflection-Agents]]"
---

# 09 — ReWOO Agents (Reasoning WithOut Observation)

## Theory

### The problem ReWOO solves
ReAct (Lesson 04) interleaves Thought → Action → Observation, one tool call at a time, with the *entire growing message history* re-sent to the model on every single step. That's simple and robust, but expensive: every tool call re-pays the cost of re-reading the whole transcript so far, and a single slow/failed tool call stalls the whole chain because the next Thought can't happen until that Observation lands.

**ReWOO (Xu et al., 2023)** asks: what if the model plans the *entire* multi-step task upfront, **before** any tool runs at all — then all tools execute, then a final synthesis step reads all results together? This decouples reasoning from observation.

### The three roles
1. **Planner** — given the task, produces a full blueprint of interlinked steps, *without* calling any tools yet. Each step is written with placeholders for evidence it depends on, e.g.:
   ```
   Plan: Find the birth year of the director of Inception.
   #E1 = Search[director of Inception]
   Plan: Use that name to find their birth year.
   #E2 = Search[birth year of #E1]
   ```
2. **Worker** — executes each planned tool call in order (substituting in prior `#E` results where a later step depends on them), collecting all evidence.
3. **Solver** — takes the full plan + all collected evidence and synthesizes the final answer in one LLM call, having never had to "reason mid-flight."

### Why this matters (the paper's actual claims)
- **~5x token efficiency** and a **4% accuracy improvement** on HotpotQA (a multi-hop QA benchmark) compared to ReAct-style observation-dependent reasoning — because the plan is written once, not re-transmitted with growing history at every step.
- **More robust under tool failure** — since the plan is fixed upfront, one failed tool call doesn't derail the model's reasoning process the way it can in ReAct (where a bad Observation directly feeds the next Thought and can send the model down a wrong path).
- **Enables offloading to smaller models** — because Planner/Worker/Solver are separable, the paper shows reasoning ability can be distilled into a much smaller model than the 175B-parameter GPT-3.5 they started from.

### The tradeoff (why ReAct is still the default for most tutorials)
ReWOO's biggest weakness: it can't adapt mid-task. If Step 2's evidence reveals the plan was wrong (e.g., the search in step 1 found an ambiguous or incorrect entity), ReWOO has no mechanism to revise the plan — it just executes it. ReAct's step-by-step observation lets it course-correct constantly; ReWOO trades that adaptability for speed and cost. **Rule of thumb:** use ReWOO-style planning for tasks with a predictable, decomposable structure (multi-hop lookups, structured research tasks); stick with ReAct for tasks where the right next step genuinely depends on what came back from the last one.

### Implementing ReWOO in LangGraph
There's no `create_rewoo_agent` prebuilt (unlike ReAct) — you build it as an explicit 3-node graph:
```
START → planner_node → worker_node (loop over plan steps, executing tools) → solver_node → END
```
- `planner_node`: one LLM call, structured output parsed into a list of `(plan_text, tool_name, tool_input, evidence_id)` steps.
- `worker_node`: iterates the plan, executing each tool call, substituting `#E1`, `#E2`, etc. placeholders with previously collected evidence before each subsequent call. This can be modeled as a small internal loop within one node, or as its own sub-graph with a counter in State.
- `solver_node`: one LLM call given the full plan + evidence, producing the final answer — no tool access here, purely synthesis.

## Important Points
- ReWOO's Worker step still needs the same tool-calling mechanics from Lesson 03 — the paradigm shift is about *when* planning happens, not how tools are invoked.
- Placeholder substitution (`#E1` referenced inside step 2's input) is the trickiest implementation detail — get your plan-parsing right or the Worker will pass literal strings like `"#E1"` into a tool instead of the actual evidence.
- Because there's no mid-task Observation feeding back into reasoning, **the Planner's prompt quality matters enormously** — a bad plan can't be corrected later the way a ReAct agent's next Thought could catch and fix a bad Action.
- Good mental model: ReAct = "improvise as you go", ReWOO = "write the whole itinerary, then execute it, then summarize the trip."

## Course Mapping
> Fill in: relevant Udemy section, if covered.

## Research/Reference
- **ReWOO: Decoupling Reasoning from Observations for Efficient Augmented Language Models** — Xu, Peng, Lei, Mukherjee, Liu, Xu. arXiv:2305.18323 (2023). Read: Section 2 (Planner/Worker/Solver breakdown), Section 4 (token efficiency + tool-failure robustness results).
- Official paper repo: `billxbf/ReWOO` on GitHub — reference implementation (not LangGraph-based, but useful for seeing the Planner/Worker/Solver prompts verbatim).

## Hands-on Labs (separate notes)
- [[09.1-Easy-ReWOO-Basic-Planner]]
- [[09.2-Medium-ReWOO-Multi-Step-Worker]]
- [[09.3-Hard-ReWOO-vs-ReAct-Benchmark]]

---
⬅ [[08-Hands-On-Labs]] | ➡ [[10-Reflection-Agents]]
