# Cross-Account Read-Only Role — Design

**Status: design only. Not deployed. No AWS API calls have been made from this repo.**

See `docs/design-plan.md` §8 for full context.

## Role spec (to be created by DevOps engineer, in the Organizations management account)

- **Name (suggested):** `FinOpsCostReadRole`
- **Trust policy:** scoped to the specific principal Claude Code's agent runs as — never a wildcard principal.
- **Permitted actions (read-only):**
  - `ce:GetCostAndUsage`, `ce:GetCostForecast`, `ce:GetReservationUtilization`, `ce:GetSavingsPlansUtilization`, `ce:DescribeCostCategoryDefinition`
  - `organizations:DescribeOrganization`, `organizations:ListAccounts`, `organizations:DescribeAccount`
  - `compute-optimizer:GetEC2InstanceRecommendations`, `compute-optimizer:GetEBSVolumeRecommendations`, `compute-optimizer:GetEnrollmentStatus`
- **Explicitly excluded:** anything mutating (`ec2:*` write, `iam:*` write, `kinesis:*` write, etc.)

## Per-account access

For accounts not covered by management-account-level Cost Explorer visibility, mirror this same read-only role in each member account, with the same scoped trust policy. This matches the pattern the CUDOS/Cloud Intelligence Dashboards Framework itself uses for multi-account aggregation.

## Before deploying

1. Confirm with DevOps engineer that this Claude Code environment actually has network reach to the company's AWS Organizations management account.
2. Confirm the specific IAM principal this role's trust policy should scope to.
3. Log the deployed role ARN and trust policy here once created — this file should be updated from "design" to "deployed" status with the real details, not left as a stale plan.

## Fallback (if live access isn't available yet)

Use manually-exported Cost and Usage Report (CUR) or Cost Explorer CSV files, dropped into `dashboard/exports/`. The `multi-account-cost-connector` skill is designed to accept either input shape.
