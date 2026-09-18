# AWS Cost Optimization Platform

Claude Code project for a real company AWS cost optimization initiative. Tracks the backlog, the skill/agent/model design, and a local Flask UI for reviewing all of it — across 10+ AWS accounts, run by 2 developers + 1 DevOps engineer on 2-week sprints.

**Status: design + skeleton. No AWS credentials have been wired up. No live AWS calls have been made from this repo.**

## Start here

- [`docs/design-plan.md`](docs/design-plan.md) — the full design plan (skill map, agent/model routing, guardrails, connectivity design, dashboard concept). Read this first.
- [`STATE.md`](STATE.md) — current status: what's built, what's pending, what's blocked on access you don't have yet.
- [`PLAN.md`](PLAN.md) — the phased rollout plan, gated on your actual company AWS/GitHub access.
- [`PROGRESS.md`](PROGRESS.md) — sprint-by-sprint log (empty until sprint 1 starts).

## How to read and modify this repo

This is a **significant, ongoing initiative** (10+ AWS accounts, 2 developers + 1 DevOps engineer, multi-sprint) — treat it like a real project's repo, not a scratch space. Concretely:

**Before changing anything:**
1. Read `STATE.md` first, every session — it separates "confirmed/done" from "designed but not built" from "genuinely blocked." Don't assume something works because a file describing it exists.
2. Check `PLAN.md` for which phase you're in — Phase 3+ (real AWS connectivity) requires explicit go-ahead per the guardrail philosophy in `docs/design-plan.md` §5; don't jump ahead of the current phase.
3. If your change is non-trivial, read [`docs/dev-methodologies/README.md`](docs/dev-methodologies/README.md) first and pick the right practice (spec first? steel-thread it? does it need an ADR?) before writing code.

**Where things live and how they connect:**
- `docs/design-plan.md` is the source of truth for architecture/agent/guardrail decisions — everything else (agents, skills, connectivity design) implements what it specifies. Change the plan first, then the implementation, not the reverse.
- `.claude/agents/` and `.claude/skills/` are read by Claude Code directly — editing an agent's `.md` frontmatter changes its model/tools/behavior the next time it's invoked.
- `backlog/{epics,features,stories}/` is currently **illustrative**, not your real backlog — see "Backlog import" below before treating it as scope.
- `connectivity/` and `automation/profile-bootstrap/` are designs, not live integrations, until Phase 3's exit condition (`PLAN.md`) is met.
- `app/` (local Flask UI) reads the above folders directly as markdown/JSON — if you restructure `backlog/` or `accounts/`, check `app/` still parses it.

**When you're done:**
- Update `STATE.md`/`PROGRESS.md` in the *same change* that changes reality — a stale status file actively misleads the next session (human or Claude). This is non-negotiable per [`docs/dev-methodologies/context-engineering.md`](docs/dev-methodologies/context-engineering.md).
- Commit to `master` in small, frequent increments per [`docs/dev-methodologies/trunk-based-development.md`](docs/dev-methodologies/trunk-based-development.md) — don't let a branch sit unmerged for days.

## Backlog import (PowerPoint + Confluence + Jira)

The 4 epics currently in `backlog/` are illustrative starters, not your real, already-defined backlog. To import the real one:
1. Connect to your company's self-hosted Confluence and Jira via MCP — see [`docs/guides/connect-confluence-gitlab-mcp.md`](docs/guides/connect-confluence-gitlab-mcp.md) for setup (this uses a community connector since this company's instances are self-hosted, not Atlassian Cloud).
2. Hand over the PowerPoint directly in a session (drag it in, or point Claude at its file path) — Claude can read it and cross-reference against Confluence/Jira content once connected.
3. Ask Claude to reconcile the PPT/Confluence/Jira content against the 4 starter epics in `backlog/epics/` — merge, replace, or keep alongside, tagging each imported item with its source for traceability (per `PLAN.md` Phase 2).

## Development methodologies (SDLC references)

[`docs/dev-methodologies/`](docs/dev-methodologies/) is a standing reference for how to do the actual development work on this project with Claude — spec-driven development, steel threading, ADRs, TDD with AI, trunk-based development, context engineering, MCP concepts, and the multi-agent orchestrator/reviewer pattern. Each file covers what it is, when it's useful (and when it's overkill), concrete steps, do's/don'ts, and primary sources — read it for actual mastery of the concept, not just to copy a recipe for this repo.

## What's in this repo

```
.claude/
  skills/          custom skills for this initiative (cost-driver-triage,
                    multi-account-cost-connector, profile-bootstrap)
  agents/          agent definitions (orchestrator, cost-analyst, wa-reviewer,
                    bootstrap-operator, sprint-planner)
backlog/
  epics/           the 4 cost-driver epics (illustrative until Phase 2 import)
  features/        features under each epic
  stories/         stories under each feature
accounts/          AWS account inventory (owners, environment tags)
connectivity/
  cross-account-role.md   cross-account IAM role design (not deployed)
  mcp-clients/            config-driven Confluence/Jira MCP registration
automation/
  profile-bootstrap/  design docs for on-demand profile automation
dashboard/         CUDOS deployment plan + space for exported CUR/CE data
docs/
  design-plan.md         source-of-truth architecture/agent/guardrail decisions
  dev-methodologies/     SDLC practice references (spec-driven dev, steel
                         threading, ADRs, TDD, trunk-based dev, MCP concepts,
                         multi-agent orchestration)
  guides/                setup guides (Confluence/Jira/GitLab MCP connectors)
app/               local Flask UI (see below)
```

## Local UI

A small Flask app to browse the backlog, skill/agent registry, and sprint view without needing any AWS connection — it reads local markdown/JSON files only.

### Run it

```bash
cd app
pip install -r requirements.txt
python app.py
```

Then open http://127.0.0.1:5060

No AWS credentials required to run the UI. It's a local review tool for the backlog and design artifacts, not a live cost dashboard — that's the separate CUDOS deployment described in `docs/design-plan.md` §10.

## Official skills installed (global, via `npx skills`)

| Skill | Source |
|---|---|
| `aws-billing-and-cost-management` | aws/agent-toolkit-for-aws |
| `aws-iam` | aws/agent-toolkit-for-aws |
| `querying-data-lake` | aws/agent-toolkit-for-aws |
| `aws-well-architected-framework-review` | aws-samples/sample-well-architected-skills-and-steering |
| `wa-guardrails` | aws-samples/sample-well-architected-skills-and-steering |

Plus skills already available in this environment, routed deliberately per `docs/design-plan.md` §5:
- **Rigor**: `fable-mode` — mandatory for `wa-reviewer`'s pass on anything account-touching, IAM-related, or feeding a stakeholder-facing savings claim.
- **Efficiency**: `caveman`, `ponytail`, `token-efficiency` — used for `orchestrator`'s routing/sequencing and `sprint-planner`'s bookkeeping, where extra reasoning spend buys nothing.

## Custom skills (this repo, `.claude/skills/`)

| Skill | Purpose |
|---|---|
| `cost-driver-triage` | Classify findings against the 4 known cost drivers, draft backlog stories |
| `multi-account-cost-connector` | Read-only cross-account cost data primitive (Cost Explorer/Organizations/Compute Optimizer) |
| `profile-bootstrap` | On-demand, time-boxed, human-approved test-profile creation (the one write-capable workflow) |

## Agents (this repo, `.claude/agents/`)

| Agent | Role |
|---|---|
| `orchestrator` | Decomposes sprint tasks, routes to the specialist below, never implements or approves — see `docs/dev-methodologies/multi-agent-orchestration.md` |
| `cost-analyst` | Read-only cost analysis specialist |
| `wa-reviewer` | Independent reviewer — proposes guardrails, never applies, never self-reviews |
| `bootstrap-operator` | The one write-capable workflow, human-approval gated |
| `sprint-planner` | Backlog bookkeeping |

## Why this isn't "done"

This was built without confirmed access to your company AWS accounts or company GitHub. Every AWS-facing piece (`connectivity/`, `automation/profile-bootstrap/`, the dashboard) is a **design**, not a working integration. See `STATE.md` for exactly what's confirmed vs. pending, and `PLAN.md` for what happens once you check your actual access.
