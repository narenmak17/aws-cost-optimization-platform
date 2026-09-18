# Multi-Agent Orchestration (Orchestrator/Reviewer Pattern)

## What it is

Instead of one agent doing analysis, implementation, and self-review, work is split across specialized agents with a distinct **orchestrator** role that coordinates and a distinct **reviewer** role that critiques — and critically, the orchestrator/reviewer is not the same agent instance that did the work. The value is independence: an agent reviewing its own output tends to confirm its own assumptions; a separate reviewing agent (or a separate pass with fresh context) is more likely to catch what the implementer missed.

This repo already has the seeds of this in its agent roster (`cost-analyst`, `wa-reviewer`, `bootstrap-operator`, `sprint-planner` — see design plan §4). What's being added is an explicit **orchestrator** agent that sits above these: routes work to the right specialist, sequences dependent steps, and hands finished work to `wa-reviewer` (or a new dedicated reviewer role) before it's considered done.

## When it's useful here

- Any sprint task that spans more than one specialist's scope — e.g., a cost-driver finding that needs `cost-analyst` to identify it, then `wa-reviewer` to check it against Well-Architected guidance, then a human to approve the resulting backlog story. An orchestrator agent sequences this instead of one session context-switching between roles.
- Any output headed for a real AWS account or a real IAM change — route it through review before it's actionable, mirroring the existing "proposes only, human merges" guardrail (design plan §5).
- Backlog/spec work pulled from Jira/Confluence (once the MCP connector is live) — an orchestrator can fan the import work out (parse PPT-derived content, cross-reference existing epics, draft stories) while a reviewer checks the drafted stories against the source before they're trusted.

## When it's overkill

- Single-file, single-concern changes with an obvious correct answer.
- Anything already gated by a steel thread or a spec review — don't stack review ceremony on top of review ceremony.

## The roles, concretely, for this project

| Role | Responsibility | Maps to |
|---|---|---|
| **Orchestrator** | Breaks a sprint task into sub-tasks, routes each to the right specialist agent, sequences dependencies, collects results | New — coordinates `cost-analyst`, `wa-reviewer`, `bootstrap-operator`, `sprint-planner` |
| **Specialist/implementer** | Does the actual analysis or drafting work | `cost-analyst`, `sprint-planner` |
| **Reviewer** | Independently checks the specialist's output against the spec/guardrails before it's accepted | `wa-reviewer` (already scoped as "proposes only, never applies") |
| **Human approval gate** | Final sign-off for anything write-capable or account-touching | You / your DevOps engineer, per design plan §5 |

## Steps

1. **Give the orchestrator a narrow job**: decompose and route, not implement. If it starts writing the actual cost analysis itself, it's collapsed back into being just another implementer.
2. **Keep the reviewer's context independent** — don't feed it the implementer's reasoning, only its output plus the spec/guardrail it should be checked against. This is what preserves the "fresh eyes" value.
3. **Make the review step a hard gate for anything account-touching or write-capable**, consistent with the existing guardrail table (design plan §5) — the orchestrator should not be able to skip straight from specialist output to "done" for these.
4. **Log what the orchestrator routed and why**, and what the reviewer flagged — this becomes part of `PROGRESS.md`'s sprint log, not just ephemeral session output.
5. **Escalate to a human when the reviewer and specialist disagree**, rather than letting the orchestrator arbitrate silently — this mirrors the ADR-worthy-decision threshold in [adr.md](./adr.md).

## Do's

- Do keep orchestrator, implementer, and reviewer as genuinely separate contexts/sessions where the stakes justify it (real AWS-account-touching work) — a review that shares the implementer's context and blind spots isn't a real review.
- Do apply this project's existing efficiency skills deliberately here: use `token-efficiency`/`ponytail` for the orchestrator's routing and bookkeeping work (cheap, mechanical), and reserve `fable-mode`'s full five-gate rigor for the reviewer's actual critique of anything cost- or security-sensitive (see [Guardrails & Skill Routing](../design-plan.md#5-guardrails--trust-boundary) and this repo's model-routing table, design plan §4) — don't run expensive rigor on cheap routing work or cheap rigor on account-touching decisions.
- Do let `sprint-planner` (Haiku 4.5, bookkeeping-only per design plan §4) handle the orchestrator's lightweight sequencing/logging work rather than a heavier model, consistent with the existing model-routing philosophy.

## Don'ts

- Don't let the orchestrator both do the work and grade its own output — that's the single failure mode this whole pattern exists to prevent.
- Don't run full multi-agent orchestration for simple, single-specialist tasks — check [When it's overkill](#when-its-overkill) first.
- Don't let review become a rubber stamp because it's run by "an agent" — the reviewer needs an actual independent spec/guardrail to check against (this is where [spec-driven development](./spec-driven-development.md) feeds directly into this pattern).

## References

- [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) — the orchestrator-workers pattern is described here as one of the core composable agent patterns.
- [Anthropic: How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) — a concrete, detailed account of an orchestrator/subagent architecture in production, including why independent review sessions catch more than self-review.
- [Anthropic: Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — relevant to why the reviewer's context should be deliberately separate from the implementer's.
