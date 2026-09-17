# AWS Cost Optimization Initiative — Design Plan

Design-only plan for the Claude Code project skeleton: SDLC process, skill/agent/model map, multi-account connectivity, and guardrails. Also published as a formatted artifact for sharing/review — ask if you need that link again.

Team: 2 developers + 1 DevOps engineer. Scope: 10+ AWS accounts. Sprint cadence: 2 weeks.

## 1. Scope, goal, assumptions

**Goal:** a Claude Code project skeleton — repo structure, skills, agents, model routing, guardrails, backlog/sprint process — for a real company AWS cost optimization program, starting from an existing PPT and a partially-built backlog.

**Assumptions (revisit if false):**
- Claude Code was installed via an IT-sanctioned process; this design doesn't route around company sandboxing.
- Existing features/stories live in a PPT and possibly Jira/Confluence, not yet in GitHub. This repo's backlog is the working backlog *for this initiative*, not an assumed system-of-record replacement.
- "Kudos dashboard" = CUDOS, a real official AWS dashboard (§10) — not a term needing invention.
- Connectivity model: Cost Explorer + Organizations API via cross-account read-only IAM role (confirmed choice, not CUR+Athena+QuickSight as primary — see §8).

## 2. Evidence base

All AWS-specific claims below were fetched from primary AWS docs/repos, not recalled from training data.

| Claim | Source |
|---|---|
| Cost Optimization Pillar: 5 design principles, 5 best-practice goal areas | [AWS WA docs](https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/design-principles.html) |
| CloudWatch Logs: Infrequent Access class ~50% cheaper, intelligent tiering to Archive after 90 days, 1 day–10 yr retention | [CloudWatch Logs billing docs](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/LogsBillingDetails.html) |
| Kinesis: provisioned mode cheaper for predictable/sustained throughput; On-Demand Advantage ~60%+ cheaper for spiky ≥10 MiB/s workloads | [AWS Big Data blog](https://aws.amazon.com/blogs/big-data/kinesis-on-demand-advantage-saves-60-on-streaming-costs/) |
| Cross-account Cost Explorer access: read-only IAM role, scoped trust policy | [Cost Management IAM docs](https://docs.aws.amazon.com/cost-management/latest/userguide/ce-access.html) |
| CUDOS / Cloud Intelligence Dashboards Framework: 20+ dashboards, multi-account aggregation, active repo | [GitHub repo](https://github.com/aws-solutions-library-samples/cloud-intelligence-dashboards-framework) |
| Compute Optimizer: org/account/region-level rightsizing preferences, 32-day lookback (June 2026) | [Compute Optimizer docs](https://docs.aws.amazon.com/compute-optimizer/latest/ug/rightsizing-preferences.html) |
| IAM Identity Center permission sets: automatable via CI/CD or Account Factory for Terraform | [AWS Integration & Automation blog](https://aws.amazon.com/blogs/infrastructure-and-automation/manage-permission-sets-and-account-assignments-in-aws-iam-identity-center-with-a-ci-cd-pipeline/) |
| SCPs + Budget Actions: auto-quarantine/auto-stop on threshold breach | [Budget Controls launch](https://aws.amazon.com/blogs/aws-cloud-financial-management/introducing-budget-controls-for-aws-automatically-manage-your-cloud-costs/) |

## 3. Skill map: install vs. build

**Install as-is (official, high-trust):** `aws-billing-and-cost-management`, `aws-iam`, `querying-data-lake` (aws/agent-toolkit-for-aws), `cost-optimization-review`/`aws-well-architected-framework-review`, `wa-guardrails` (aws-samples/sample-well-architected-skills-and-steering).

**Build custom, on top of the above:**
- `cost-driver-triage` — classifies findings against the 4 named drivers, drafts stories in this repo's backlog format.
- `multi-account-cost-connector` — read-only cross-account data primitive; the one place the read-only trust boundary is enforced.
- `profile-bootstrap` — on-demand, time-boxed, human-approved test-profile creation. Genuinely novel; nothing in the skill registry covers this workflow.

**Decision, logged as rationale:** no single monolithic skill/agent. Mixing read-only analysis with write-capable automation collapses the trust boundary and works against the token-saving goal.

## 4. Agent & model routing

| Agent | Model | Tools | Trust level |
|---|---|---|---|
| `cost-analyst` | Sonnet | multi-account-cost-connector, cost-driver-triage, aws-billing-and-cost-management | Read-only |
| `wa-reviewer` | Sonnet, escalate to Opus for cross-account architecture calls | cost-optimization-review, wa-guardrails, architecture-decision-record | Proposes only — never applies |
| `bootstrap-operator` | Sonnet + mandatory human approval | profile-bootstrap, aws-iam | Write-capable — the one exception |
| `sprint-planner` | Haiku 4.5 | sprint-backlog-sync | Bookkeeping only |

## 5. Guardrails & trust boundary

Following the `wa-guardrails` pattern (preventive + detective, tied to a control ID) rather than an invented philosophy:
- No agent gets standing write access to any AWS account (Cost Explorer role is read-only).
- Profile bootstrap requires human (DevOps) approval before any IAM change.
- No agent applies an SCP/Config rule directly — proposals only, human merges and deploys.
- AWS Budget Actions + SCP triggers as an independent backstop against runaway test-account spend.
- Every architecture decision logged via `architecture-decision-record`.

## 6. Repo skeleton

See this repo's actual structure — `.claude/skills/`, `.claude/agents/`, `backlog/{epics,features,stories}/`, `accounts/`, `connectivity/`, `automation/profile-bootstrap/`, `dashboard/`, `docs/`, `app/`.

## 7. Backlog & sprint model

Epic → Feature → Story, mapped to GitHub Milestones/Issues/labels. One-time import of the existing PPT-derived backlog, tagged with source for traceability. 2-week sprints; DevOps owns connectivity/bootstrap/guardrail-deployment stories, developers own analysis-skill work and dashboard build-out; cost-driver remediation split by account/service.

## 8. AWS connectivity design

Cross-account read-only IAM role (`FinOpsCostReadRole`) in the Organizations management account, scoped trust policy, `ce:*`/`organizations:Describe*`/`compute-optimizer:Get*` only — no mutating actions. **Fallback path:** manually-exported CUR/Cost Explorer CSV when live access isn't confirmed yet — do not assume the happy path.

## 9. Profile bootstrapping automation

On-demand, parameterized request (account, purpose, duration) → mapped to an existing IAM Identity Center permission-set shape → DevOps approval → time-boxed assignment (default 5 business days) → auto-revoke on expiry. This is the actual fix for profile sprawl, not a policy asking people to clean up.

## 10. Cost dashboard — CUDOS

"Kudos dashboard" = CUDOS, part of AWS's official open-source Cloud Intelligence Dashboards Framework. Foundational tier needs only CUR via Athena/Glue; Advanced tier adds Trusted Advisor, Health Events, Organizations, Compute Optimizer. Deploy CUDOS as the stakeholder-facing surface; Cost Explorer API (§8) stays the interactive/automation surface — same underlying billing data, different consumers.

## 11. The four named cost drivers

| Driver | Verified tooling | Backlog shape |
|---|---|---|
| Over-provisioned EC2 | Compute Optimizer rightsizing | Feature per account/group |
| Verbose CloudWatch logging | Infrequent Access class, tiering, retention policy | Feature per environment/log group |
| Kinesis provisioned-capacity misuse | Classify predictable vs. spiky before recommending a mode change — provisioned mode is *correctly* cheaper for steady load | Story = classify first, then rightsize shards or evaluate on-demand |
| Test-team profile sprawl | IAM Identity Center + on-demand bootstrap | Feature = the automation build; recurring story = stale-profile audit |

## 12. Risks, rejected alternatives, open questions

**Rejected:** CUR+Athena+QuickSight as primary connector (heavier setup); one monolithic skill/agent (trust-boundary collapse); installing low-install third-party FinOps skills directly (official skills already cover the ground, with security audits).

**Open questions:** confirm actual AWS network/credential reach for this Claude Code instance; who owns creating `FinOpsCostReadRole`; where the existing features/stories currently live (Jira/Confluence/PPT only).

## 13. What happens next

See `PLAN.md` for the phased rollout, gated on access confirmation.
