# AWS Account Inventory

**Status: template — not yet filled in with real account data.**

Fill in once you have the actual list of 10+ accounts in scope. Do not commit real account IDs if this repo might ever go public — it's currently private, but treat account IDs with the same care as any other internal identifier.

| Account ID | Alias | Environment | Owner | Notes |
|---|---|---|---|---|
| _(fill in)_ | | prod / non-prod / test | | |

## Environment tagging convention

Recommend tagging accounts (or at minimum tracking here) as one of: `prod`, `staging`, `non-prod`, `test`. The test-team profile sprawl driver (epic-04) specifically concerns `test`-tagged accounts — having this table accurate is a prerequisite for that epic's stories to be scoped correctly.
