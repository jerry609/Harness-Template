# AGENTS.md

This file routes agents to the right artifacts. It is not the full knowledge base.

## Read in this order

1. `README.md`
2. `docs/architecture/index.md`
3. The active file in `docs/product-specs/`
4. The matching file in `docs/exec-plans/`
5. `docs/quality/golden-principles.md`
6. `artifacts/progress.md`
7. `artifacts/feature-list.json`
8. `evals/README.md`

## Load on demand (do not read unless the current task requires it)

- `docs/architecture/boundaries.md` — when touching module boundaries
- `docs/architecture/context-budget.md` — when context is running low
- `docs/architecture/multi-session.md` — when planning multi-session work
- `docs/architecture/multi-agent.md` — when coordinating multiple agents
- `docs/architecture/tech-selection.md` — when choosing technologies
- `docs/architecture/progressive-disclosure.md` — when managing prompt complexity
- `docs/quality/linter-guide.md` — when writing or modifying lint rules
- `docs/quality/debugging-agent-failures.md` — when an agent is failing repeatedly
- `skills/` — when the task matches a specific skill

## Operating rules

- Hidden context does not count. If it matters, put it in the repo.
- Start from a spec and a plan before making large changes.
- Keep one session focused on one feature, bug, or cleanup theme.
- Prefer small diffs with explicit verification steps.
- Update progress, feature state, and decisions before ending a session.
- Repeated review feedback should become docs, scripts, or CI rules.
- Escalate only when judgment, production access, or missing secrets are required.
- Run `python scripts/check_boundaries.py` and `python scripts/lint_agent_friendly.py` before committing.
- When an agent struggles, treat it as an environment bug — see `docs/quality/debugging-agent-failures.md`.

## Session loop

1. Load the active spec, plan, and progress files.
2. Confirm the current feature state in `artifacts/feature-list.json`.
3. Execute one coherent slice of work.
4. Verify the result with tests, smoke checks, or environment feedback.
5. Record what changed in `artifacts/progress.md`.
6. Update `artifacts/decisions.md` if a durable tradeoff was made.
7. Leave the repo in a clean, reproducible state.

## Definition of done

A task is only done when all of the following are true:

- The relevant spec and plan are up to date.
- The implementation has outcome-oriented verification.
- `artifacts/progress.md` reflects the latest state.
- `artifacts/feature-list.json` has the correct status.
- Any new durable rule is captured in docs or automation.