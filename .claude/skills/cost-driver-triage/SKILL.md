---
name: cost-driver-triage
description: Triage AWS cost findings against this company's four known cost drivers (over-provisioned EC2, verbose CloudWatch logging, Kinesis provisioned-capacity misuse, test-team profile sprawl) and draft them as backlog stories in the epic/feature/story format this repo uses. Use when reviewing Cost Explorer/Compute Optimizer output and deciding whether a finding is worth a story, and if so, what shape.
---

# Cost Driver Triage

Turns raw cost/usage findings into backlog stories, scoped to the four drivers this program tracks. Does not call AWS directly — takes data already pulled by `multi-account-cost-connector` or a manually exported CUR/Cost Explorer CSV.

## The four drivers and how to classify a finding under each

### 1. Over-provisioned EC2
- Evidence: Compute Optimizer rightsizing recommendation with "Over-provisioned" finding, or sustained CPU/memory utilization well below instance capacity over the lookback window (14–32 days).
- Story shape: one story per account (or account-group) — "Review Compute Optimizer findings for `<account>`, produce rightsizing PR for flagged instances."
- Do not story an instance Compute Optimizer marks "Optimized" or "Under-provisioned" — that is not this driver.

### 2. Verbose CloudWatch logging
- Evidence: log group ingestion volume/cost disproportionate to its retention value; DEBUG-level logs retained in production; no retention policy set (defaults to "Never Expire").
- Story shape: one story per log group or per environment — "Set retention + log class policy for `<log group / environment>`."
- Check whether Infrequent Access log class or intelligent tiering is already applicable before proposing a retention cut — cheaper storage class may solve it without losing data.

### 3. Kinesis provisioned-capacity misuse
- **This driver requires classification before recommending a fix.** Provisioned mode is the AWS-recommended, cheaper choice for steady, predictable throughput. Do not treat "provisioned mode" itself as the waste.
- Evidence to check: CloudWatch shard-level utilization metrics (`IncomingBytes`, `IncomingRecords` vs. provisioned shard capacity) over at least 2 weeks.
- If utilization is steady and near capacity: not a story — stream is correctly configured.
- If utilization is steady but shard count is oversized relative to actual throughput: story = "rightsize shard count for `<stream>`."
- If utilization is spiky/unpredictable and aggregate throughput is low: story = "evaluate On-Demand Standard for `<stream>`."
- If aggregate throughput is high (≥10 MiB/s) or the account runs hundreds of streams: story = "evaluate On-Demand Advantage for `<stream/account>`."

### 4. Test-team profile sprawl
- Evidence: IAM Identity Center permission-set assignments or CLI profiles with no activity in 30+ days; profiles created outside the `profile-bootstrap` workflow.
- Story shape: recurring story type, not one-off — "Audit and revoke stale test profiles in `<account>`" — schedule this every sprint, not just once.

## Output format

Each triaged finding becomes a story with this shape, ready to hand to `sprint-backlog-sync`:

```
Title: <driver-tagged, account-scoped action>
Epic: <one of the 4 driver epics>
Evidence: <what data supports this — cite the metric/report, not a guess>
Proposed action: <specific, not "optimize costs">
Estimated impact: <$ or % if the source data supports it; otherwise "not yet quantified">
```

Do not draft a story without evidence attached. "Looks over-provisioned" is not a story; a Compute Optimizer finding ID or a specific CloudWatch metric query result is.
