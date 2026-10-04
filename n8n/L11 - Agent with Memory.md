---
tags: [n8n, lab, tier3, ai, memory]
difficulty: 4
time: 90 min
---
# L11 - Agent with Memory

**Goal:** Give an agent memory so it remembers earlier turns in a conversation.

**Concepts:** Memory nodes, session keys, context window limits, why memory is per session.

## Steps
1. Start from L10. Add a **Simple Memory** node to the agent's memory input.
2. Test: tell the agent your name, then ask it to recall the name in the next message.
3. Set the session key so that two separate chat sessions do not share memory. Test by opening a second chat window.
4. Set the memory window to 4 messages. Ask about something from 6 turns ago and observe the failure.

> [!hint]- Hint 1
> Memory keyed to a fixed value is shared by every user. Key it to a session or user ID for real use.

## Reflection
- What did the 4-message window cost you, and how would you decide the right size for a real support bot?
