---
tags: [n8n, community-nodes, policy]
---
# 05 - Community Nodes and Policy

## What They Are
Community nodes are npm packages built by third parties that add integrations to n8n. You install them from **Settings → Community Nodes**, using a package name that starts with `n8n-nodes-`.

## Likely Constraints at Work
- Your company may disable community nodes entirely. Check the instance's Settings page first. If the menu is missing, that is your answer.
- Installing packages on a shared VM can need admin approval because each one runs code with access to your workflows and credentials.
- Unverified packages are a supply-chain risk. Prefer verified ones and read the source repository.

## Options That Need No New Packages
Most of the labs above use only built-in nodes. For anything custom, use:
- **Code node** for JavaScript logic.
- **HTTP Request** for any REST API, which covers most third-party services.
- **Execute Command** only if your admin enables it, because it runs shell commands on the host.

## Candidate Packages to Evaluate (verify before use)
Look these up on npm and check their maintenance status and last publish date:
- Community packages for text extraction or PDF parsing, if you need them in L12-style pipelines.
- Vendor-maintained integrations for tools your team already uses.

## Request Template for IT
> Hi, I'd like to learn n8n for internal automation. Could you confirm whether community nodes are enabled on our instance? If yes, I'd like to request approval for `[package name]` for [purpose]. I'll only use it in a sandbox workflow with no production credentials.
