# Steel Threading (Walking Skeleton)

## What it is

A "steel thread" (also called a walking skeleton) is the thinnest possible end-to-end slice through a system that proves the architecture actually works — one request, one account, one path, touching every layer (auth, network, data, UI) — before building out breadth or polish. The term comes from proving a single thread can bear load before weaving the whole fabric.

The distinction from a spike: a steel thread is production-quality code on a narrow path, meant to be kept and extended — not throwaway exploration.

## When it's useful here

- **Before wiring `multi-account-cost-connector` to all 10+ AWS accounts.** Steel-thread it: one read-only IAM role, one account, one Cost Explorer call, one row rendered in the local Flask UI. That proves the IAM trust policy, the network path, and the data shape all work together before scaling to the rest.
- **Before building the CUDOS dashboard deployment.** One dashboard widget backed by one exported CUR file, end-to-end, before the full Cloud Intelligence Dashboards Framework rollout.
- Any time `STATE.md` lists something as "genuinely blocked on access you don't have yet" — a steel thread is the concrete way to find out, cheaply, whether the blocker is real or assumed.

## When it's overkill

- When the architecture is already proven (e.g., the 2nd, 3rd, 4th AWS account after the 1st one worked) — that's scaling out a proven thread, not threading a new one.
- Pure UI/copy changes with no new integration surface.

## Steps

1. **Pick the thinnest possible path that still exercises every architectural layer** you're unsure about. For this project: one account → one IAM role → one API call → one data transform → one UI row.
2. **Build it for real** — not mocked, not stubbed. If the steel thread mocks the AWS call, it hasn't actually tested the thing you're unsure about (IAM trust, network reach, permission scope).
3. **Time-box it.** If the steel thread can't be proven within a day or two, that's itself a signal — the blocker is bigger than assumed, escalate rather than let it become an unbounded spike.
4. **Once it works, write down what it proved** (this is where it hands off to an ADR — see [adr.md](./adr.md)) — e.g., "cross-account read role works from this Claude Code instance's network, confirmed 2026-09-XX."
5. **Then widen** — go from 1 account to all 10+, from 1 dashboard row to the full CUDOS deployment — using the proven thread as the template, not by redesigning from scratch.

## Do's

- Do pick the riskiest unknown as the thing the thread proves — for this repo, that's currently "does this Claude Code instance have network reach to company AWS accounts at all" (STATE.md's own open question).
- Do keep the steel thread's code — it becomes the seed of the real implementation, not a prototype you throw away.
- Do report the result plainly: it worked, it didn't, or it's blocked on X — this is exactly the calibrated-reporting habit this repo already uses in STATE.md.

## Don'ts

- Don't steel-thread something you're not actually unsure about — that's just building the feature slowly.
- Don't mock the risky part to make the thread "pass" — a steel thread that mocks AWS IAM tells you nothing about whether IAM actually works.
- Don't skip straight to full breadth (all 10+ accounts) without a proven thread first — that's how `connectivity/cross-account-role.md` stays a design doc that fails in a surprising way on account #7.

## References

- [Alistair Cockburn: Walking Skeleton](https://wiki.c2.com/?WalkingSkeleton) — the original pattern description.
- [Martin Fowler: Steel Thread](https://martinfowler.com/bliki/DesignStaminaHypothesis.html) (related concept discussion) and general agile literature on walking skeletons as the first vertical slice.
- [Growing Object-Oriented Software, Guided by Tests](http://www.growing-object-oriented-software.com/) — Freeman & Pryce's book, which popularized "walking skeleton" as a concrete first step in a new system's development.
