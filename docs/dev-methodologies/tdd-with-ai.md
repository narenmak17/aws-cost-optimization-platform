# Test-Driven Development with AI (AI-TDD)

## What it is

Standard TDD (red-green-refactor) with one addition specific to AI-assisted coding: the tests are written and reviewed by a human (or at least reviewed before being trusted) *before* the AI writes implementation code against them. This matters because an AI asked to "write code and tests" for the same feature at the same time will often write tests that simply confirm whatever the implementation happens to do — passing tests that don't actually verify correctness.

The failure mode this defends against: an LLM-generated cost-savings recommendation that looks plausible, compiles, and passes a self-generated test, but is wrong in a way that only a domain-aware human test would catch.

## When it's useful here

- **`cost-driver-triage`'s classification logic** — the mapping from raw cost data to "this is EC2 rightsizing waste" vs. "this is Kinesis over-provisioning" is exactly the kind of logic that can look right and be subtly wrong.
- **Any IAM policy generation** in `profile-bootstrap` or `connectivity/` — a wrong IAM policy is a security bug, not just a functional one; write the test for "does NOT grant X" before generating the policy.
- **Savings calculations** feeding the CUDOS dashboard — a wrong number here is worse than no number, per this user's own standing principle about calibrated, cited claims.

## When it's overkill

- Markdown-only changes (backlog stories, docs).
- The local Flask UI's read-only display logic, where a visual check is faster and just as reliable as a unit test.

## Steps

1. **Write the test first, from the spec** (see [spec-driven-development.md](./spec-driven-development.md)) — not from a first draft of the implementation. Ask: "what would make this wrong?" before "what would make this pass?"
2. **Have a human review the test** before implementation starts, especially for anything touching cost calculations or IAM — this is the cheap point to catch "you tested the happy path only."
3. **Let the AI implement against the test**, iterating until it's green, without changing the test to fit the implementation.
4. **Explicitly ask for edge cases and negative cases** — an AI given "write tests for this" will default to happy-path coverage unless prompted for boundary conditions, error states, and "this must never happen" cases (e.g., "test that profile-bootstrap never creates a role with broader-than-read permissions").
5. **Refactor only with tests green**, and re-run after every AI-driven refactor — AI refactors can silently change behavior while "cleaning up" code.

## Do's

- Do write tests that would fail against a plausible-but-wrong implementation, not just against "did nothing happen."
- Do have a human sanity-check tests for anything cost- or security-sensitive before trusting the AI to implement against them.
- Do ask explicitly for edge/negative cases — don't assume the AI infers them.

## Don'ts

- Don't let the same AI session write both the test and the implementation without a review checkpoint in between — that removes the independence that makes TDD catch real bugs.
- Don't accept "tests pass" as sufficient evidence for cost/savings claims — cross-check a sample against the source data manually, per this repo's own doc-discipline rule.
- Don't skip tests for IAM/permission code because "it's just a design doc for now" — once `connectivity/cross-account-role.md` becomes real code, it needs tests before it touches a real account.

## References

- [Kent Beck: Test-Driven Development by Example](https://www.oreilly.com/library/view/test-driven-development/0321146530/) — the canonical TDD reference; AI-TDD is this discipline applied with an LLM as implementer.
- [Anthropic: Claude Code best practices](https://www.anthropic.com/engineering/claude-code-best-practices) — covers test-first workflows specifically for agentic coding sessions.
- [Martin Fowler: On the diverse and gradual evolution of TDD in the AI era](https://martinfowler.com/articles/exploring-gen-ai.html) — discussion of how TDD's value proposition shifts (and in some ways strengthens) with AI-generated code.
