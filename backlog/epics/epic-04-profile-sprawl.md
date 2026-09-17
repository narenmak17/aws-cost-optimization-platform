---
id: epic-04
title: Access governance — test profile sprawl
driver: test-profile-sprawl
status: draft
---

# Epic 04: Access Governance

Multiple ad-hoc AWS CLI profiles created per account by the test team, driving both access risk and forgotten-resource cost. See `docs/design-plan.md` §9, §11.

## Features

- `feature-04-01`: Profile bootstrap automation (on-demand, time-boxed)
- `feature-04-02`: Recurring stale-profile audit

## Notes

Illustrative starter — not yet reconciled with the existing PPT backlog (see `STATE.md`). `feature-04-01` is the build target for the `profile-bootstrap` skill itself.
