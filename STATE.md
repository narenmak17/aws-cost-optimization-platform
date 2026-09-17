# State

Last updated: 2026-09-17

## Confirmed / done

- Private GitHub repo created: `narenmak17/aws-cost-optimization-platform`
- Design plan written and reviewed once (see `docs/design-plan.md`), grounded in verified AWS Well-Architected / FinOps sources (citations in plan §2)
- Repo skeleton scaffolded: `.claude/`, `backlog/`, `accounts/`, `connectivity/`, `automation/`, `dashboard/`, `docs/`, `app/`
- 3 custom skills drafted: `cost-driver-triage`, `multi-account-cost-connector`, `profile-bootstrap`
- 4 agent definitions drafted: `cost-analyst`, `wa-reviewer`, `bootstrap-operator`, `sprint-planner`
- Official AWS skills installed (global): `aws-billing-and-cost-management`, `aws-iam`, `querying-data-lake`, `aws-well-architected-framework-review`, `wa-guardrails`
- 4 backlog epics drafted (one per cost driver), with starter features/stories
- Local Flask UI built — backlog/skill/agent/sprint browser, no AWS dependency

## Not done — genuinely blocked on access you don't have yet

- **AWS connectivity is not wired up.** No IAM role has been created, no AWS profile has been configured, no live Cost Explorer/Organizations/Compute Optimizer call has been made. `connectivity/cross-account-role.md` is a design spec, not a deployed role.
- **No confirmation this Claude Code instance has network reach to your company's AWS accounts at all.** This was flagged as an open question in the design plan (§12) and is still open.
- **CUDOS dashboard is not deployed.** `dashboard/cudos-deployment-plan.md` describes the approach; nothing has been run against the `cloud-intelligence-dashboards-framework` CloudFormation/CLI tooling.
- **`profile-bootstrap` automation is design-only.** No IAM Identity Center permission set has been created or modified.
- **Existing PPT backlog has not been imported.** The 4 epics/features/stories in `backlog/` are illustrative starters written from the design plan's cost-driver analysis, not a migration of your actual, already-defined features/stories. That import still needs to happen once you tell me where those currently live (Jira/Confluence/only the PPT — this was an open question in the design plan, still unanswered).
- **`wa-guardrails` and `aws-well-architected-framework-review` skills are installed but unused** — no review has been run against a real workload because no real AWS account is connected yet.

## Decisions locked so far

- Connectivity model: Cost Explorer + Organizations API via cross-account read-only IAM role (your choice, not CUR+Athena+QuickSight as primary)
- Repo owner: personal GitHub (`narenmak17`), not a company org
- No monolithic skill/agent — split by read-only vs. write-capable trust boundary (see design plan §3–§5)
- Kinesis driver requires per-stream classification before recommending a capacity-mode change — provisioned mode is not assumed to be the waste

## Next real decision point

Once you check your actual company AWS/GitHub access (flagged as pending in our last exchange), this file's "not done" list should shrink or get rescoped — some items may turn out to already be partly available via company-provided tooling we haven't accounted for yet. Re-read this file and the design plan before assuming anything below the "confirmed" line still holds.
