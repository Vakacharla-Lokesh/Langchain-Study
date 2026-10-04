---
tags: [labs, practice, capstone]
prev: "[[07-Tavily-LangSmith-External-Tools]]"
next: "[[00-Index]]"
---

# 08 — Hands-On Practice Labs (Full Bank)

> This file collects every lab linked from Lessons 01–07 into one progression, plus a capstone. Do them **in order within each level** — each lab assumes the skills/code from the previous ones. Check off as you go.

## How to use this
- **Easy** labs = confirm you understood the mechanics. Should take under an hour each.
- **Medium** labs = combine 2-3 concepts, first real "build something" labs.
- **Hard** labs = production-shaped problems: error handling, multi-tool coordination, observability. These double as portfolio-worthy pieces.
- For each lab: note the **agent loop shape** required (none / manual tool loop / LangGraph ReAct) so you don't over- or under-build.

---

## 🟢 Easy Labs

- [ ] **E1 — LCEL warm-up** *(Lesson 01)*: `prompt \| model \| StrOutputParser` chain summarizing pasted text into exactly 3 bullets. *Loop shape: none, single invoke.*
- [ ] **E2 — Parallel chain** *(Lesson 01)*: `RunnableParallel` generating a tweet + LinkedIn post + haiku from one topic in a single call. *Loop shape: none.*
- [ ] **E3 — Few-shot formatting** *(Lesson 02)*: `FewShotPromptTemplate` forcing consistent JSON output via examples alone (no structured-output API). *Loop shape: none.*
- [ ] **E4 — Manual windowed memory** *(Lesson 02)*: Keep only last 4 messages in a chat loop; prove something said 6 turns back is "forgotten." *Loop shape: simple chat loop, no tools.*
- [ ] **E5 — First tool call** *(Lesson 03)*: 2 math tools bound to a model, manually execute the single resulting tool call. *Loop shape: single tool call, no loop yet.*
- [ ] **E6 — Visible Thoughts** *(Lesson 04)*: Add an explicit `Thought:` instruction to your Lesson-03 hand-rolled loop; compare tool selection with/without it across 5 runs. *Loop shape: manual tool loop.*
- [ ] **E7 — Linear LangGraph** *(Lesson 05)*: 3-node linear graph: outline → paragraph → tweet. Print `print_ascii()`. *Loop shape: DAG, no cycle.*
- [ ] **E8 — Checkpointed cycle** *(Lesson 06)*: Add `MemorySaver` to the Lesson-05 Hard lab's draft/critique loop; inspect `get_state_history`. *Loop shape: cyclic graph + persistence.*
- [ ] **E9 — Real search, traced** *(Lesson 07)*: Single-tool Tavily `create_react_agent` on a time-sensitive question; find the run in LangSmith. *Loop shape: LangGraph ReAct (prebuilt).*

**Hints/Suggestions:**
- E5/E6: print the raw `response.tool_calls` object before executing anything — seeing the exact structure demystifies the whole mechanism.
- E7: always render the graph before running it — catches wiring mistakes before runtime errors do.
- E9: if Tavily returns nothing useful, check the query the model actually generated (visible in the LangSmith trace) — often the fix is prompt wording, not the tool.

---

## 🟡 Medium Labs

- [ ] **M1 — Multi-field structured extraction** *(Lesson 01)*: `.with_structured_output()` extracting `{sentiment, dishes_mentioned, rating_out_of_5}` from a review paragraph, with `.with_fallbacks()` to a second model. *Loop shape: none.*
- [ ] **M2 — Summarization memory** *(Lesson 02)*: Every 5 turns, compress history via a separate LLM call; log token savings. *Loop shape: chat loop with periodic side-call.*
- [ ] **M3 — Full hand-rolled tool loop** *(Lesson 03)*: 3 tools, manual `while` loop (call model → check tool_calls → execute → append ToolMessage → repeat) until no tool_calls remain. **This is the conceptual keystone lab of the whole vault — do not skip.**
- [ ] **M4 — Multi-hop ReAct** *(Lesson 04)*: 2-tool agent (fake search + calculator) answering a question requiring search → extract → search → extract → calculate. Print the full trace.
- [ ] **M5 — Conditional routing graph** *(Lesson 05)*: Classify input as question/complaint, route to different response nodes. *Loop shape: branching DAG, no cycle.*
- [ ] **M6 — Hand-built vs prebuilt ReAct** *(Lesson 06)*: Build the same 2-tool agent both as a manual `StateGraph` and via `create_react_agent`; diff outputs on 5 test questions.
- [ ] **M7 — Search + calculator combo, traced** *(Lesson 07)*: Tavily + calculator tool answering a question needing both; verify the LangSmith trace matches the expected ReAct sequence.

**Hints/Suggestions:**
- M3: this is exactly what `create_react_agent` does internally — write it before you use the shortcut, or the abstraction will feel like magic instead of a convenience.
- M4/M7: keep your fake "documents" dict small (3-5 entries) so you can predict exactly what the agent *should* find, making it easy to spot when it goes wrong.
- M6: if outputs diverge between hand-built and prebuilt, the usual culprit is a subtly different system prompt or message ordering — diff those first.

---

## 🔴 Hard Labs

- [ ] **H1 — Resilient noisy-search agent** *(Lesson 04)*: ReAct agent with a search tool that returns irrelevant results ~30% of the time; agent must recognize bad results in its Thought and retry with a reformulated query, capped at 6 iterations with graceful "could not find" fallback.
- [ ] **H2 — Human-in-the-loop side-effect agent** *(Lesson 06)*: Agent with a fake `send_email` tool, `interrupt_before=["tools"]` pausing before execution, human approves/rejects/edits args via CLI input, resumes via `update_state()`.
- [ ] **H3 — Three-tool agent with evaluation set** *(Lesson 07)*: Tavily + custom API tool (your choice) + `PythonREPLTool`; build a 5-question LangSmith eval dataset and score pass/fail.
- [ ] **H4 — Error-recovery structured extractor** *(Lesson 01+03 combo)*: A tool-using agent whose tool sometimes throws (simulate a flaky external API); errors are returned as `ToolMessage` content, and the agent must self-correct without explicit retry code.

**Hints/Suggestions:**
- H1: to simulate "30% noisy," just use `random.random() < 0.3` inside your fake search tool to swap in an irrelevant canned result — deterministic enough to debug, random enough to test recovery.
- H2: the trickiest part is usually resuming correctly — `graph.invoke(None, config)` (passing `None` as input) continues from the interrupt point using the already-saved state; don't re-pass the original input.
- H3: you don't need LangSmith's formal `evaluate()` API for this to count — a script that loops the 5 questions, checks expected substrings in the final answer, and prints a pass/fail table is a legitimate first version. Upgrade to formal LangSmith evaluators once comfortable.
- H4: resist the urge to add a `try/except` with manual retry logic around the tool call itself — the whole point is proving the *agent's reasoning* handles the recovery, not your Python.

---

## 🏆 Capstone (after all of the above)
Build a **"Research Assistant" ReAct agent** that:
- Uses Tavily for live web search
- Uses a custom tool of your choice (pick something relevant to your CGPA/portfolio angle — e.g., a GitHub API tool that looks up repo stats, or an arXiv tool for paper lookups)
- Runs as a LangGraph `StateGraph` (hand-built, not the prebuilt helper — proves you actually understand the wiring)
- Has a checkpointer so it remembers context across multiple questions in one session
- Has `interrupt_before` on any tool call you'd consider "risky" (define your own bar)
- Is fully traced in LangSmith with at least one saved evaluation dataset
- README explains the agent-loop diagram (Thought/Action/Observation) in your own words, citing the ReAct paper

This is portfolio-shaped on purpose — worth polishing into something you can point to in interviews, given the job-search context.

---
⬅ [[07-Tavily-LangSmith-External-Tools]] | 🏠 [[00-Index]]
