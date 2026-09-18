# State

Last updated: 2026-09-18

## Confirmed / done

- Private GitHub repo created: `narenmak17/aws-cost-optimization-platform`
- Design plan written and reviewed once (see `docs/design-plan.md`), grounded in verified AWS Well-Architected / FinOps sources (citations in plan §2)
- Repo skeleton scaffolded: `.claude/`, `backlog/`, `accounts/`, `connectivity/`, `automation/`, `dashboard/`, `docs/`, `app/`
- 3 custom skills drafted: `cost-driver-triage`, `multi-account-cost-connector`, `profile-bootstrap`
- 5 agent definitions drafted: `orchestrator` (new, coordinates/routes only), `cost-analyst`, `wa-reviewer`, `bootstrap-operator`, `sprint-planner`
- Official AWS skills installed (global): `aws-billing-and-cost-management`, `aws-iam`, `querying-data-lake`, `aws-well-architected-framework-review`, `wa-guardrails`
- 4 backlog epics drafted (one per cost driver), with starter features/stories
- Local Flask UI built — backlog/skill/agent/sprint browser, no AWS dependency
- README.md enriched with a "how to read and modify this repo" section, backlog-import steps, and links to the new methodology references
- `docs/dev-methodologies/` created: spec-driven development, steel threading, ADRs, TDD with AI, trunk-based development, context engineering, MCP concepts (mastery reference), multi-agent orchestration — each with when-useful/when-overkill, steps, do's/don'ts, and cited sources
- Confluence/Jira MCP connector guide corrected for **self-hosted (Data Center)** instances — the original guide assumed Atlassian Cloud, which doesn't apply here; now documents the `sooperset/mcp-atlassian` community server with PAT auth
- Config-driven MCP client scaffolding added: `connectivity/mcp-clients/config.example.json` + `register_atlassian_mcp.py`, so connection details live in a reviewable file instead of ad-hoc CLI flags
- Guardrails (`docs/design-plan.md` §5) now explicitly name skill routing: `fable-mode` mandatory for `wa-reviewer`'s account-touching/stakeholder-facing reviews, `token-efficiency`/`ponytail` for `orchestrator`/`sprint-planner` bookkeeping

## Not done — genuinely blocked on access you don't have yet

- **AWS connectivity is not wired up.** No IAM role has been created, no AWS profile has been configured, no live Cost Explorer/Organizations/Compute Optimizer call has been made. `connectivity/cross-account-role.md` is a design spec, not a deployed role.
- **No confirmation this Claude Code instance has network reach to your company's AWS accounts at all.** This was flagged as an open question in the design plan (§12) and is still open.
- **CUDOS dashboard is not deployed.** `dashboard/cudos-deployment-plan.md` describes the approach; nothing has been run against the `cloud-intelligence-dashboards-framework` CloudFormation/CLI tooling.
- **`profile-bootstrap` automation is design-only.** No IAM Identity Center permission set has been created or modified.
- **Existing PPT/Confluence/Jira backlog has not been imported.** The 4 epics/features/stories in `backlog/` are illustrative starters, not a migration of your actual features/stories. Blocked on: (1) you handing over the PowerPoint directly, and (2) you completing the self-hosted Atlassian MCP connector setup in `docs/guides/connect-confluence-gitlab-mcp.md` (requires your own PAT — I cannot generate or approve that for you).
- **The Confluence/Jira MCP connector is documented and scaffolded, but not connected.** `register_atlassian_mcp.py` has not been run — it requires you to create a Data Center Personal Access Token and populate `connectivity/mcp-clients/config.json` (git-ignored, copy from `config.example.json`) yourself.
- **`wa-guardrails` and `aws-well-architected-framework-review` skills are installed but unused** — no review has been run against a real workload because no real AWS account is connected yet.
- **The new `orchestrator` agent is defined but untested** — it hasn't yet coordinated a real multi-specialist sprint task.

## Decisions locked so far

- Connectivity model: Cost Explorer + Organizations API via cross-account read-only IAM role (your choice, not CUR+Athena+QuickSight as primary)
- Repo owner: personal GitHub (`narenmak17`), not a company org
- No monolithic skill/agent — split by read-only vs. write-capable trust boundary (see design plan §3–§5)
- Kinesis driver requires per-stream classification before recommending a capacity-mode change — provisioned mode is not assumed to be the waste
- Atlassian instances are self-hosted (Data Center), not Cloud — use `sooperset/mcp-atlassian` with PAT auth, not `mcp.atlassian.com`
- Agent roster now includes a dedicated `orchestrator` (coordinates/routes only) separate from `wa-reviewer` (reviews only) — neither role does the other's job, and `orchestrator` cannot bypass `wa-reviewer` for account-touching work

## Next real decision point

Two things need you specifically, not another Claude Code session: (1) create a Confluence/Jira Data Center PAT and run `register_atlassian_mcp.py --run` to actually connect the backlog-import path; (2) hand over the PowerPoint file so it can be cross-referenced against whatever Confluence/Jira surfaces. Once you check your actual company AWS/GitHub access (still pending from a prior session), the AWS-connectivity portion of the "not done" list should shrink or get rescoped. Re-read this file and the design plan before assuming anything below the "confirmed" line still holds.
