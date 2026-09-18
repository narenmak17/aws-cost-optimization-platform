# Spec-Driven Development (SDD)

## What it is

Spec-Driven Development flips the usual AI-coding order: instead of prompting for code and iterating on the diff, you write a structured specification first — the *what* and *why*, with explicit requirements, constraints, and acceptance criteria — and treat that spec as the durable source of truth. The AI (and human reviewers) implement *against* the spec, and the spec gets updated when reality forces a change, not silently abandoned once code exists.

The core problem it solves: an LLM has no persistent memory of *why* a decision was made once the conversation that produced it scrolls out of context or a new session starts. A spec is the artifact that survives that gap.

## When it's useful here

- Before starting any backlog epic/feature/story that will actually get built (not the current illustrative starters in `backlog/`).
- Before wiring `multi-account-cost-connector` to a real AWS account — the spec should nail down exactly which APIs, which permissions, which accounts, before any code is written.
- Anytime a Confluence/Jira story is vague enough that two developers (or a developer and Claude) could reasonably build two different things from it.

## When it's overkill

- One-line fixes, config tweaks, or anything reversible in under 5 minutes.
- Exploratory spikes where the point is to learn what's possible, not to commit to a design.

## Steps

1. **Write the spec before touching code.** Structure: problem statement, explicit requirements (numbered, testable), non-goals, constraints (e.g., "read-only IAM only," "no live AWS calls until Phase 3"), and acceptance criteria.
2. **Store it as a file in the repo**, not just in chat — e.g., `backlog/features/feature-XX/spec.md`. This repo's `docs/design-plan.md` is already a spec at the project level; individual features/stories should get the same treatment at their scale.
3. **Review the spec with a human before implementation starts.** This is the cheap-to-change stage; catching a wrong assumption here costs a re-read, not a re-write.
4. **Implement against the spec**, referencing it explicitly in the session ("implement per `spec.md` §3") so the AI's context is anchored to the written requirements, not to a paraphrase.
5. **When implementation reveals the spec was wrong or incomplete, update the spec in the same change**, don't just patch the code and leave the spec stale — a stale spec is worse than no spec because it actively misleads the next reader.
6. **Use the spec as the acceptance check** — did the delivered story satisfy the numbered requirements, yes/no, not "does it look right."

## Do's

- Do write specs at the altitude where ambiguity actually causes rework — usually feature/story level, not task level.
- Do keep specs in version control alongside the code they govern, so a `git blame`/history shows how intent evolved.
- Do make acceptance criteria testable ("returns cost data for a single account within 5s" not "works well").
- Do let a spec be short — a half-page spec that's actually read beats a ten-page one that isn't.

## Don'ts

- Don't write a spec and then let the implementation drift from it without updating either.
- Don't treat the spec as immutable — it's a living document until the story ships, then it's a historical record.
- Don't spec things that are genuinely exploratory — that's what a steel thread or a spike is for (see [steel-threading.md](./steel-threading.md)).
- Don't let the AI infer requirements from the codebase when a spec should exist but doesn't — flag the gap and write the spec first.

## References

- [GitHub: Spec-Driven Development with AI — Concepts and Methodology](https://github.com/github/spec-kit) — GitHub's own open-source toolkit and write-up on SDD, the most concrete practitioner reference as of 2026.
- [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) — the underlying reasoning for why structured upfront specs reduce agentic drift.
- [AWS: Spec-driven development with AI coding assistants](https://aws.amazon.com/blogs/devops/spec-driven-development-with-ai-coding-assistants/) — AWS's own framing, relevant given this project's AWS focus.
