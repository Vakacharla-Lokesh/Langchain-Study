---
tags: [n8n, lab, tier2, http, api]
difficulty: 3
time: 90 min
---
# L06 - API Chaining

**Goal:** Call one API, use its output to call a second API, and combine the results.

**Concepts:** HTTP Request in depth, headers, query parameters, pagination, authentication types.

## Steps
1. Call a public API such as `https://jsonplaceholder.typicode.com/users`.
2. For each user, call `https://jsonplaceholder.typicode.com/users/{{ $json.id }}/posts`. Use a loop-free approach first, then notice the item count.
3. Use an **Aggregate** or Code node to produce one object per user with `name` and `postCount`.
4. Add a header `Accept: application/json` and a query parameter `_limit=3` to see how each is set.

> [!hint]- Hint 1
> If the second HTTP node runs once per user, that is correct. Items fan out automatically.

> [!hint]- Hint 2
> To inspect a 401 or 429 response, enable the node's "Full Response" option so you can read the status and headers.

## Stretch
Find a public API that requires an API key or bearer token, store the token as a credential, and call it without pasting the token into a field.

## Reflection
- What is the difference between a query parameter and a header, and where does each belong?
