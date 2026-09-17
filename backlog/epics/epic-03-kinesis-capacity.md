---
id: epic-03
title: Streaming cost reduction — Kinesis capacity mode
driver: kinesis-provisioned-capacity
status: draft
---

# Epic 03: Streaming Cost Reduction

Kinesis Data Streams capacity-mode review. See `docs/design-plan.md` §11 — provisioned mode is not assumed wasteful; every story here starts with per-stream utilization classification before recommending a mode change.

## Features

- `feature-03-01`: Per-stream utilization classification (steady vs. spiky)
- `feature-03-02`: Shard rightsizing for confirmed-steady streams
- `feature-03-03`: On-Demand evaluation for confirmed-spiky/low-throughput streams

## Notes

Illustrative starter — not yet reconciled with the existing PPT backlog (see `STATE.md`).
