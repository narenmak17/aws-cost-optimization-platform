# Model Routing Table

Consult when delegating work to subagents, workers, or other models. Edit the rows to match your own toolkit — the scores below are placeholders for you to fill in from your own testing, not claims about any model.

Score each model 1–5 on:

- **Cost** — higher score means cheaper per unit of work
- **Intelligence** — comprehension, code review quality, holding a long context together
- **Taste** — creativity, UI/UX judgment, non-obvious approaches

| Model | Cost | Intelligence | Taste | Route here for |
|---|---|---|---|---|
| _(frontier / orchestrator)_ | | | | Scoping, adversarial review, architecture, final verification |
| _(mid-tier)_ | | | | Implementation from a clear plan, refactors, test writing |
| _(cheap / fast)_ | | | | Scouting: file search, grep-and-report, log triage, summarizing large inputs |
| _(local / open source)_ | | | | Offline work, privacy-sensitive input, bulk mechanical edits |

## Routing rules

- The orchestrator does Gates 1–3 and Gate 4. Workers execute and report.
- Send a worker one narrow task with an explicit success condition and an explicit output format. Vague instructions to a cheap model are where the savings evaporate.
- Scouting work — "find every call site of X and paste the surrounding five lines" — is the highest-leverage delegation. It is mechanical, verifiable, and consumes the most context.
- Never delegate the final verification pass. A worker's report of success is evidence to check, not a result to accept.
- Escalate a task up a tier when a worker's output fails verification twice. Re-prompting a model that has already missed twice usually costs more than escalating once.
