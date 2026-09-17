---
name: profile-bootstrap
description: Design/workflow for on-demand, time-boxed AWS test-profile creation via IAM Identity Center permission sets, instead of the test team hand-creating standing CLI profiles per account. This is the one write-capable workflow in the repo and requires human approval before any IAM change is made. Use when a team member requests test access to an AWS account.
---

# Profile Bootstrap

Replaces ad-hoc, standing AWS CLI profiles (the actual driver of test-team cost sprawl — see `docs/design-plan.md` §9 and §11) with parameterized, on-demand, time-boxed access.

## This is the one write-capable path in this repo

Every other skill here is read-only or produces a proposal for a human to apply. This skill is the exception — it results in an actual IAM Identity Center permission-set assignment. Because of that:

- **No automatic execution.** A request must be explicitly approved by the DevOps engineer before the assignment is created. Do not skip this gate to save time.
- **Time-boxed by default.** Every assignment gets an expiry (default: 5 business days, matching a sprint's typical test cycle — override only with an explicit reason attached to the request).
- **Scoped, not broad.** Map the request to the narrowest existing permission-set "shape" that covers it. Do not create a new permission set per request; that recreates the sprawl this workflow exists to prevent.

## Request shape

```
Requestor: <name>
Account(s): <specific account ID(s), never "all accounts">
Purpose: <what test activity this supports>
Duration: <default 5 business days, or justified override>
Permission-set shape requested: <existing shape name, e.g. "test-readonly", "test-write-nonprod">
```

## Workflow

1. Requestor submits the request shape above.
2. `profile-bootstrap` validates: does an existing permission-set shape cover this? If not, flag for a human to define a new shape — do not improvise one.
3. Request routed to DevOps engineer for approval.
4. On approval: permission-set assignment created via IAM Identity Center, with the stated expiry.
5. On expiry: assignment auto-revokes. This is the mechanism that actually prevents sprawl — not a policy document asking people to clean up after themselves.

## Recurring audit

Independent of new requests, run a periodic check (see `cost-driver-triage` driver 4) for assignments that exist outside this workflow entirely — profiles created before this system existed, or created by someone bypassing it. Flag those for manual revocation review; do not auto-revoke without a human looking first, since some may be legitimate standing access this workflow didn't originate.
