---
name: multi-account-cost-connector
description: Read-only primitive for pulling AWS cost and usage data across 10+ accounts via a cross-account IAM role (Cost Explorer, Organizations, Compute Optimizer). Use whenever an agent needs current cost/usage data from more than one AWS account, instead of each skill reimplementing STS role assumption.
---

# Multi-Account Cost Connector

A single, consistent way to reach cost data across every account in scope. Every other skill in this repo that needs live AWS data goes through this one, so the read-only boundary lives in exactly one place.

## Trust boundary — read this before touching credentials

This skill is **read-only by design**. It must never be extended with write/mutating AWS calls (no `ec2:StopInstances`, no `iam:CreateRole`, no `kinesis:UpdateShardCount`). If a task needs a write action, that belongs to a separate, human-approved workflow (see `profile-bootstrap` for the one write-capable path this repo defines). Mixing read and write in this skill collapses the trust boundary the whole guardrail design depends on — see `docs/design-plan.md` §5.

## Connectivity model

1. A dedicated IAM role (e.g. `FinOpsCostReadRole`) exists in the AWS Organizations management account, or as a delegated-admin role.
2. Trust policy is scoped to a specific principal — never a wildcard.
3. Permitted actions: `ce:Get*`, `ce:Describe*`, `organizations:Describe*`, `organizations:List*`, `compute-optimizer:Get*`. Nothing else.
4. For accounts not covered by the management-account role directly, assume a per-account role scoped the same way — mirrors the pattern the CUDOS/Cloud Intelligence Dashboards Framework uses for multi-account aggregation.

## Before assuming live access works

Confirm actual connectivity state first — do not assume every session has AWS network/credential reach. Check:
- Is an AWS profile or role configured in this environment at all? (`aws sts get-caller-identity`)
- Can it reach the org's management account?

If either check fails, use the **fallback path**: operate against a manually-exported CUR file or Cost Explorer CSV placed in `dashboard/exports/`. Every skill that consumes this connector should accept either a live pull or a static export as input — don't hard-code an assumption that live access is available.

## What this skill returns

Normalized cost/usage records: account ID, service, cost, usage type, time period. Downstream skills (`cost-driver-triage`) consume this shape regardless of whether it came from a live API call or a static export.
