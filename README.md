# AWS Cost Optimization Platform

Claude Code project for a real company AWS cost optimization initiative. Tracks the backlog, the skill/agent/model design, and a local Flask UI for reviewing all of it — across 10+ AWS accounts, run by 2 developers + 1 DevOps engineer on 2-week sprints.

**Status: design + skeleton. No AWS credentials have been wired up. No live AWS calls have been made from this repo.**

## Start here

- [`docs/design-plan.md`](docs/design-plan.md) — the full design plan (skill map, agent/model routing, guardrails, connectivity design, dashboard concept). Read this first.
- [`STATE.md`](STATE.md) — current status: what's built, what's pending, what's blocked on access you don't have yet.
- [`PLAN.md`](PLAN.md) — the phased rollout plan, gated on your actual company AWS/GitHub access.
- [`PROGRESS.md`](PROGRESS.md) — sprint-by-sprint log (empty until sprint 1 starts).

## What's in this repo

```
.claude/
  skills/          custom skills for this initiative (cost-driver-triage,
                    multi-account-cost-connector, profile-bootstrap)
  agents/          agent definitions (cost-analyst, wa-reviewer,
                    bootstrap-operator, sprint-planner)
backlog/
  epics/           the 4 cost-driver epics
  features/        features under each epic
  stories/         stories under each feature
accounts/          AWS account inventory (owners, environment tags)
connectivity/      cross-account IAM role design (not deployed)
automation/
  profile-bootstrap/  design docs for on-demand profile automation
dashboard/         CUDOS deployment plan + space for exported CUR/CE data
docs/              design plan, this repo's source-of-truth docs
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

Plus token-efficiency skills already available in this environment: `caveman`, `ponytail`, `token-efficiency`.

## Custom skills (this repo, `.claude/skills/`)

| Skill | Purpose |
|---|---|
| `cost-driver-triage` | Classify findings against the 4 known cost drivers, draft backlog stories |
| `multi-account-cost-connector` | Read-only cross-account cost data primitive (Cost Explorer/Organizations/Compute Optimizer) |
| `profile-bootstrap` | On-demand, time-boxed, human-approved test-profile creation (the one write-capable workflow) |

## Why this isn't "done"

This was built without confirmed access to your company AWS accounts or company GitHub. Every AWS-facing piece (`connectivity/`, `automation/profile-bootstrap/`, the dashboard) is a **design**, not a working integration. See `STATE.md` for exactly what's confirmed vs. pending, and `PLAN.md` for what happens once you check your actual access.
