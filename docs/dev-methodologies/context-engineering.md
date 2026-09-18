# Context Engineering for Multi-Session AI Work

## What it is

Context engineering is the deliberate practice of curating what an AI agent sees at the start of a session — not just prompting well within a session, but structuring the repo, its docs, and its state so that a fresh session (with zero memory of prior ones) can reconstruct the right context quickly and correctly. It's the practice that makes an LLM's lack of persistent memory a non-problem.

This repo already practices this: `STATE.md`, `PLAN.md`, and `PROGRESS.md` exist specifically so a new session reads three short files and knows exactly what's confirmed, what's pending, and what's genuinely blocked — instead of re-deriving it from file timestamps or guessing.

## When it's useful here

- Every session on this repo, structurally — this project spans weeks/months and multiple contributors (human and AI), so no single session's context window can hold the full history.
- Especially important before Phase 3 (real AWS connectivity) — a session that skips reading STATE.md's "genuinely blocked on access" section risks re-attempting something already known to be blocked, or worse, assuming access exists.

## When it's overkill

- It's rarely overkill to maintain — the risk is under-investment, not over-investment. The failure mode to avoid is writing context docs once and letting them go stale.

## Steps

1. **Maintain a small set of always-read files** at the repo root: status (STATE.md), plan (PLAN.md), and a running log (PROGRESS.md). Keep each one short enough to read in under a minute.
2. **Write for a reader with zero prior context** — no "as discussed," no unexplained shorthand. Assume the reader (human or AI) is cold.
3. **Separate what's confirmed from what's designed-but-not-built** — this repo's STATE.md already does this explicitly ("Confirmed / done" vs. "Not done — genuinely blocked"). Keep that separation strict; it's the single highest-value habit here.
4. **Update these files in the same change that changes reality** — don't let STATE.md say "not done" for something that was actually finished three commits ago (a documented recurring failure mode in this user's other projects — orphaned-draft/stale-status patterns).
5. **Link outward instead of duplicating** — STATE.md links to `docs/design-plan.md` rather than restating it; keep a single source of truth per fact.
6. **At the start of a new session on a multi-week project, read the status files before doing anything else** — this is the concrete behavior context engineering is asking for.

## Do's

- Do keep status/plan/progress files short and current — a 30-second read is the target.
- Do explicitly separate "confirmed" from "designed" from "blocked" — vague status is worse than no status.
- Do treat a stale status file as a bug, not a documentation nicety.

## Don'ts

- Don't let context accumulate only in chat history — if it's not in a file, the next session doesn't have it.
- Don't write status docs that require the reader to already know the project — every file should stand alone.
- Don't let "done" claims outlive the code — verify against the actual filesystem/git state before trusting a status line (a standing rule from this user's other projects).

## References

- [Anthropic: Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — Anthropic's own framing of context engineering as the discipline that replaced "prompt engineering" for agentic work.
- [Anthropic: Claude Code best practices](https://www.anthropic.com/engineering/claude-code-best-practices) — includes concrete guidance on CLAUDE.md-style repo memory files.
- [12-Factor Agents](https://github.com/humanlayer/12-factor-agents) — community reference on building reliable LLM applications, several factors of which map directly to context/state management practices.
