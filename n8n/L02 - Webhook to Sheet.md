---
tags: [n8n, lab, tier1, webhook]
difficulty: 2
time: 60 min
---
# L02 - Webhook to Sheet

**Goal:** Receive form submissions over HTTP and store them in a spreadsheet.

**Concepts:** Webhook trigger, test vs production URL, `.body` payloads, app nodes, credentials.

## Steps
1. Create a Google Sheet with columns `timestamp, name, email, source`. If your company blocks Google, use a sheet or table in your VM's database instead, or ask IT for an approved target.
2. Add a **Webhook** trigger with method `POST`. Copy the **Test URL**.
3. Add a **Google Sheets** node set to *Append Row*. Map each column with expressions such as `{{ $json.body.name }}`.
4. Send a test with curl:
   ```bash
   curl -X POST "<TEST_URL>" -H "Content-Type: application/json" \
     -d '{"name":"Asha","email":"asha@example.com","source":"curl"}'
   ```
5. Add an **Edit Fields** node before the sheet to normalize the email to lowercase.
6. Activate the workflow and call the **Production URL** instead.

> [!hint]- Hint 1
> A 404 on the production URL usually means the workflow is not activated.

> [!hint]- Hint 2
> If `name` shows as undefined, check whether the field sits at `$json.body.name` or `$json.name` in the Webhook output.

> [!hint]- Hint 3
> Lowercase an email with `{{ $json.body.email.toLowerCase() }}`.

## Checkpoint
- A POST creates exactly one new row, and a second POST creates a second row.

## Stretch
Add a **Respond to Webhook** node that returns `{"status":"saved"}` with HTTP 201.

## Reflection
- Why are there two URLs, and when would you use each?
