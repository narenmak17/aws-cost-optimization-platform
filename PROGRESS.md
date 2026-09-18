# Progress Log

Sprint-by-sprint log. Empty until sprint 1 actually starts (see `PLAN.md` Phase 2).

## 2026-09-17 — Repo setup (pre-sprint)

- Design plan reviewed
- Repo skeleton, custom skills, agent definitions, README/STATE/PLAN, local Flask UI created
- Not yet a sprint — no committed backlog scope yet

## 2026-09-18 — SDLC references, orchestrator agent, MCP connector correction (pre-sprint)

- README enriched: "how to read and modify this repo" guidance, backlog-import steps, methodology links
- `docs/dev-methodologies/` created (8 files): spec-driven dev, steel threading, ADRs, TDD with AI, trunk-based dev, context engineering, MCP concepts, multi-agent orchestration
- Corrected `docs/guides/connect-confluence-gitlab-mcp.md`: company Atlassian is self-hosted (Data Center), not Cloud — replaced the Cloud-only setup with `sooperset/mcp-atlassian` (PAT-based) and added config-driven client scaffolding (`connectivity/mcp-clients/`)
- Added `orchestrator` agent (coordinates/routes only) and updated `wa-reviewer` to name `fable-mode` as mandatory for account-touching/stakeholder-facing reviews; `docs/design-plan.md` §4–§5 updated to match
- Still not a sprint — no committed backlog scope yet; backlog import still blocked on the user providing the PowerPoint and running the MCP connector setup themselves
