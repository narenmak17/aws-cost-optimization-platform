# Rollout Plan

Phased, gated on actual access confirmation — not a fixed calendar. Each phase's start condition is explicit so this doesn't silently assume access that hasn't been checked yet.

## Phase 0 — Design (done)

- Design plan reviewed (`docs/design-plan.md`)
- Repo skeleton, custom skills, agent definitions, local Flask UI built
- **Exit condition:** you've reviewed this repo's structure and the design plan, and corrected anything wrong before real AWS/company resources get touched.

## Phase 1 — Access confirmation (next, blocking everything after it)

- Confirm whether this Claude Code instance has network reach to your company's AWS accounts (open question from design plan §12)
- Confirm where your existing features/stories actually live today (PPT only? Jira? Confluence?) so the backlog import in Phase 2 is scoped correctly
- Identify who owns creating the cross-account `FinOpsCostReadRole` — likely your DevOps engineer, but needs an explicit named owner
- Confirm company GitHub org vs. personal repo placement is acceptable for where this actually needs to live long-term (this repo currently sits under your personal GitHub per your instruction — flag if that needs to move to a company org before real account data touches it)
- **Exit condition:** you and your DevOps engineer know, concretely, what AWS access exists today and what needs to be requested.

## Phase 2 — Backlog import + sprint 1 setup

- Import your actual existing features/stories from wherever they live (Phase 1 answer) into `backlog/`, tagged with their source for traceability
- Reconcile against the 4 illustrative starter epics already in this repo — merge, replace, or keep alongside as appropriate
- Set up GitHub Issues/Projects if that's the chosen backlog tool (design plan §7), or confirm this repo's markdown-based backlog is sufficient for now
- Plan sprint 1 using the local Flask UI's backlog view
- **Exit condition:** sprint 1 has a real, non-illustrative backlog and a committed scope.

## Phase 3 — Connectivity (only after Phase 1 confirms access exists)

- DevOps engineer creates `FinOpsCostReadRole` per `connectivity/cross-account-role.md`
- Test read-only Cost Explorer/Organizations/Compute Optimizer calls against 1 account before rolling out to all 10+
- If live access isn't available yet: use the fallback path (manually exported CUR/Cost Explorer CSV into `dashboard/exports/`) so analysis work isn't blocked waiting on IAM provisioning
- **Exit condition:** `multi-account-cost-connector` skill has been tested against at least one real account, or the fallback path is confirmed as the interim approach.

## Phase 4 — Cost driver remediation (ongoing, sprint-by-sprint)

- Run `cost-driver-triage` against real data for the 4 known drivers (EC2, CloudWatch, Kinesis, profile sprawl)
- Convert findings into real backlog stories, replacing the illustrative ones
- First remediation PRs (rightsizing, log retention policy, Kinesis classification, stale profile audit)

## Phase 5 — Automation + dashboard

- Build `profile-bootstrap` workflow for real, with DevOps approval gate wired to an actual notification path (Slack/email — not yet decided)
- Deploy CUDOS (Cloud Intelligence Dashboards Framework) per `dashboard/cudos-deployment-plan.md`
- Decide on sharing mechanism for the "kudos"/savings dashboard with stakeholders

## What does NOT happen automatically

No phase here executes itself. Each phase starts when you say so, especially Phase 3 onward — anything that touches real AWS accounts gets your explicit go-ahead first, per the guardrail design in the plan (§5).
