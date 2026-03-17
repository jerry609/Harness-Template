# Decisions

## 2026-03-17 - Keep `AGENTS.md` thin

- Context: Agent-first repositories decay when the routing file becomes a dumping ground.
- Decision: Keep `AGENTS.md` focused on reading order, operating rules, and done criteria.
- Consequences: Durable knowledge belongs in `docs/`, `artifacts/`, or automation.

## 2026-03-17 - Prefer outcome-oriented verification

- Context: Agent narration can sound correct even when the environment is wrong.
- Decision: Organize verification around eval tasks, smoke checks, and environment state.
- Consequences: Add real tests and graders as soon as the project scope is clear.
