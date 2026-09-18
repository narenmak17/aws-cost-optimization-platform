# Architecture Decision Records (ADRs)

## What it is

An ADR is a short, immutable, numbered document that records one architectural decision: the context that forced it, the decision itself, and the consequences (including what was rejected and why). Once written, an ADR isn't edited to reflect new information — if a decision is superseded, you write a new ADR that supersedes the old one, so the history of *why* things changed stays intact.

This project's `STATE.md` "Decisions locked so far" section is already doing this informally. ADRs formalize it: one decision per file, permanent, cross-referenced.

## When it's useful here

- Every decision `STATE.md` currently lists under "Decisions locked so far" should really be its own ADR — e.g., "Connectivity model: Cost Explorer + Organizations API via cross-account role, not CUR+Athena+QuickSight."
- Any time a Claude Code session and a human disagree on approach and the human's call wins — write down *why*, so the next session (human or AI) doesn't re-litigate it from scratch.
- Rejected alternatives are worth recording too — e.g., if pglogical-style replication is rejected for a security reason (see this user's Payment Initiation Platform precedent), that reasoning belongs in an ADR so it isn't silently re-proposed six months later.

## When it's overkill

- Reversible, low-stakes choices (variable naming, which local port a dev server uses).
- Decisions already fully captured by a spec (see [spec-driven-development.md](./spec-driven-development.md)) — don't duplicate, just link.

## Steps

1. **Create `docs/adr/NNNN-short-title.md`**, numbered sequentially (`0001-`, `0002-`, ...).
2. **Use a minimal fixed structure**: Status (proposed/accepted/superseded), Context (what forced the decision), Decision (what was chosen), Consequences (what this makes easier/harder, what was rejected and why).
3. **Never edit an accepted ADR's Decision section after the fact.** If circumstances change, write a new ADR, set its Status to "supersedes ADR-000X," and mark the old one "superseded by ADR-00XY."
4. **Link ADRs from the artifact they govern** — e.g., `connectivity/cross-account-role.md` should link to the ADR that decided the connectivity model.
5. **Reference the ADR number in commit messages and PRs** when a change implements or revisits a decision, so `git log` and the ADR trail cross-reference each other.

## Do's

- Do keep each ADR to about half a page — the goal is a reference, not an essay.
- Do record rejected alternatives with their actual reasons — "rejected X because Y" is the highest-value sentence in the whole document.
- Do number and index them (`docs/adr/README.md` as a table of contents) so they're discoverable without reading every file.

## Don'ts

- Don't rewrite history — supersede, don't edit, once an ADR is accepted.
- Don't write an ADR for every decision — reserve it for ones that are expensive to reverse or non-obvious to a future reader (the same bar this repo already applies to its own memory-writing discipline).
- Don't let ADRs live only in a wiki disconnected from the code — keep them in-repo so they version with the code they explain.

## References

- [Michael Nygard: Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) — the original ADR proposal.
- [adr.github.io](https://adr.github.io/) — community-maintained ADR templates, tooling, and examples.
- [AWS Prescriptive Guidance: Architecture Decision Records](https://docs.aws.amazon.com/prescriptive-guidance/latest/architecture-decision-records/welcome.html) — AWS's own ADR guidance, relevant given this project's AWS scope.
