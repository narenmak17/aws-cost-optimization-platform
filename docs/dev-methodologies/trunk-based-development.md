# Trunk-Based Development

## What it is

All developers (and AI sessions) commit to a single shared branch (`master`/`main`) in small, frequent increments, using short-lived feature branches (hours to a couple of days, not weeks) merged behind feature flags or guarded by incompleteness rather than long-lived divergence. The alternative it replaces is GitFlow-style long-lived feature branches that accumulate merge conflicts and drift from trunk.

## When it's useful here

- As soon as this repo has more than one active contributor to reconcile — currently: 2 developers + 1 DevOps engineer, plus however many Claude Code sessions are touching the repo across a sprint.
- Specifically relevant because **AI sessions branch and iterate quickly** — a Claude Code session working on a feature for an hour can generate many small commits; trunk-based practice says merge that back frequently rather than letting it become a long-lived branch that conflicts with another session's parallel work on `multi-account-cost-connector`.

## When it's overkill

- Never really overkill for a repo with more than one contributor — the question is usually *how* to apply it (branch lifetime, flag strategy), not *whether* to.

## Steps

1. **Keep feature branches short-lived** — target merging back to `master` within a day. If a Claude Code session's task will take longer, break it into smaller steel-threaded increments (see [steel-threading.md](./steel-threading.md)) that can each merge independently.
2. **Gate incomplete work behind explicit incompleteness markers**, not long-lived branches — e.g., a half-built `multi-account-cost-connector` merges to trunk marked clearly as design-only in STATE.md, rather than living on a branch for weeks.
3. **Rebase/merge from trunk frequently** into any active branch, so an AI session's context always reflects the latest merged state, not a week-stale snapshot.
4. **Run checks before merge** — even lightweight ones (does the Flask app still start, do markdown links resolve) — catching breakage at merge time, not at the next session's start.
5. **Delete branches after merge** — don't accumulate stale branches that confuse which one is "the current work."

## Do's

- Do merge small and often — this pairs directly with steel threading's "thinnest slice first" instinct.
- Do keep `master` always in a state a new Claude Code session (or new developer) can safely start from.
- Do use PR review even for AI-authored changes, per this repo's existing guardrail discipline (design plan §5).

## Don'ts

- Don't let a Claude Code session accumulate days of uncommitted or unmerged work — the longer a branch diverges, the harder the next session's context-gathering becomes.
- Don't use long-lived environment branches (`dev`, `staging` as permanent branches) — prefer trunk + deployment gating.
- Don't skip small merges "because it's not done yet" — incomplete-but-safe is mergeable; broken is not.

## References

- [Trunk Based Development (trunkbaseddevelopment.com)](https://trunkbaseddevelopment.com/) — the canonical reference site, patterns for short-lived branches and branch-by-abstraction.
- [Google: Why Google Stores Billions of Lines of Code in a Single Repository](https://research.google/pubs/why-google-stores-billions-of-lines-of-code-in-a-single-repository/) — background on trunk-based practice at scale.
- [DORA (DevOps Research and Assessment): Trunk-based development](https://dora.dev/capabilities/trunk-based-development/) — the empirical case that trunk-based development correlates with higher-performing teams.
