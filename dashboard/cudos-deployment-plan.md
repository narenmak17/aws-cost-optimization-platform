# CUDOS Dashboard — Deployment Plan

**Status: design only. Not deployed.**

"Kudos dashboard" from the original ask = **CUDOS** (Cost and Usage Dashboard Operations Solution), part of AWS's official [Cloud Intelligence Dashboards Framework](https://github.com/aws-solutions-library-samples/cloud-intelligence-dashboards-framework). See `docs/design-plan.md` §10.

## What it needs

- **Foundational tier:** AWS Data Exports (CUR 2.0), Amazon Athena + Glue for querying. No extra infra beyond what's typically already present.
- **Advanced tier** (recommended for this initiative, since it directly serves the 4 known cost drivers): additionally needs Trusted Advisor data, AWS Health Events, Organizations data, Compute Optimizer insights.

## Deployment steps (not yet executed)

1. Confirm CUR 2.0 (Data Exports) is enabled in the management account.
2. Deploy via CloudFormation template or the framework's CLI tool (PyPI-distributed) — framework claims under-30-minutes setup.
3. Configure multi-account aggregation: the framework's data-collection Lambda assumes a role in each linked account — this can reuse or sit alongside the `FinOpsCostReadRole` design in `connectivity/cross-account-role.md`, but check the framework's own IAM requirements before assuming full overlap.
4. Point QuickSight at the deployed dashboards.

## Relationship to the Cost Explorer connector (§8)

CUDOS is CUR-based; the `multi-account-cost-connector` skill uses the Cost Explorer/Organizations API directly. These are not competing — CUDOS is the always-on, shareable dashboard for stakeholders (the "share with leadership" surface); the Cost Explorer path is the agent's interactive/automation surface. Both read from the same underlying billing data.

## Exports directory

`dashboard/exports/` — drop manually-exported CUR/Cost Explorer CSVs here if live connectivity isn't confirmed yet (see `connectivity/cross-account-role.md` fallback section). Not committed with real data — see `.gitignore`.
