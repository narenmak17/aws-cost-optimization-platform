# Development Methodologies for AI-Assisted SDLC

This folder is a reference set for running this project's development lifecycle *with* Claude Code, not just documenting what Claude Code happens to produce. Each file covers one methodology: what it is, when it earns its place here, the concrete steps, do's/don'ts, and primary sources.

These are practices, not tools. None of them require a specific skill or MCP server — they're ways of structuring work so that an LLM collaborator (and your two developers + one DevOps engineer) stay aligned on scope, intent, and risk across sessions that don't share memory by default.

## Why this project needs this folder specifically

This repo already does some of this instinctively:

- `STATE.md` / `PROGRESS.md` are an informal decision log — see [Architecture Decision Records](./adr.md) for the formal version.
- `PLAN.md`'s phase-gating ("Phase 3 only after Phase 1 confirms access") is a steel-thread instinct — see [Steel Threading](./steel-threading.md).
- The design plan (`docs/design-plan.md`) with its numbered, citable sections is close to a spec — see [Spec-Driven Development](./spec-driven-development.md) for how to make that formal and durable across AI sessions.

Read the methodology doc before the pattern name gets used loosely in planning conversations — "let's steel-thread this" or "write an ADR for that" should mean something specific and repeatable, not just "let's be careful."

## Index

| Methodology | Use it when | File |
|---|---|---|
| Spec-Driven Development (SDD) | Before building anything non-trivial with AI — turns intent into a durable, reviewable artifact the AI implements against | [spec-driven-development.md](./spec-driven-development.md) |
| Steel Threading (Walking Skeleton) | Before committing to full multi-account/multi-service build-out — prove one thin end-to-end path first | [steel-threading.md](./steel-threading.md) |
| Architecture Decision Records (ADRs) | Any time a decision is made that's expensive to reverse or non-obvious to a future reader | [adr.md](./adr.md) |
| Test-Driven Development with AI (AI-TDD) | Writing remediation logic, IAM policy generators, or anything where "it compiled" isn't "it's correct" | [tdd-with-ai.md](./tdd-with-ai.md) |
| Trunk-Based Development | Once more than one person (or more than one Claude session) is committing to this repo | [trunk-based-development.md](./trunk-based-development.md) |
| Context Engineering for Multi-Session AI Work | Any work that spans more than one Claude Code session — which is most of this project | [context-engineering.md](./context-engineering.md) |
| MCP Concepts (mastery reference) | Understanding how the Confluence/Jira/GitLab connectors actually work under the hood, not just the setup commands | [mcp-concepts.md](./mcp-concepts.md) |
| Multi-Agent Orchestration (Orchestrator/Reviewer) | Sprint work spanning more than one specialist, or anything account-touching that needs independent review before it's trusted | [multi-agent-orchestration.md](./multi-agent-orchestration.md) |

## How these fit together on this project

A realistic sprint here looks like:

1. **Spec** the sprint's target story (SDD) — pull from Jira/Confluence via the Atlassian MCP connector (see `docs/guides/connect-confluence-gitlab-mcp.md`), not from memory of the PPT.
2. If the story touches new AWS surface area (a new account, a new API), **steel-thread** it — one account, one read-only call, one row in the dashboard — before generalizing to all 10+ accounts.
3. Any time the steel thread or the spec forces a real decision (which IAM trust policy, which backlog tool, which model to route a skill to) — **write an ADR**. Don't let it live only in chat history.
4. Anything that classifies, computes savings, or generates a policy — build it **test-first**, because a plausible-looking recommendation that's wrong is worse than no recommendation.
5. Keep the repo on **trunk-based** short-lived branches so Claude sessions and human developers aren't reconciling long-lived divergent branches.
6. Across all of it, apply **context engineering** discipline — this repo's STATE.md/PLAN.md pattern *is* that discipline; the file just makes explicit why it works and how to keep doing it as the repo grows.

## Do's and don'ts across all of them

**Do:**
- Treat every methodology here as a forcing function for writing things down in a file, not a ceremony for its own sake.
- Re-read the relevant doc before invoking the pattern by name in a planning conversation, so "spec it" or "steel-thread it" means the same thing every time.
- Cite sources when a design claim is load-bearing (this repo's own doc-discipline rule — see project memory).

**Don't:**
- Don't apply all of them to every change. A one-line config fix doesn't need a spec, an ADR, and a steel thread.
- Don't let a methodology doc go stale silently — if a linked source moves or a practice changes (e.g., a new Claude Code feature makes something easier), update the file, don't just keep citing the old approach.
- Don't use these as a substitute for the actual guardrails in `docs/design-plan.md` §5 (the write-capable vs. read-only trust boundary) — methodology governs *how* you build, not *what* you're allowed to touch.
