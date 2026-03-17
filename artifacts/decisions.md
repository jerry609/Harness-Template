# Decisions

## 2026-03-17 - Keep `AGENTS.md` thin

- Context: Agent-first repositories decay when the routing file becomes a dumping ground.
- Decision: Keep `AGENTS.md` focused on reading order, operating rules, and done criteria.
- Consequences: Durable knowledge belongs in `docs/`, `artifacts/`, or automation.

## 2026-03-17 - Prefer outcome-oriented verification

- Context: Agent narration can sound correct even when the environment is wrong.
- Decision: Organize verification around eval tasks, smoke checks, and environment state.
- Consequences: Add real tests and graders as soon as the project scope is clear.

## 2026-03-17 - Mechanical enforcement over documentation-only rules

- Context: OpenAI's harness engineering found that agents drift when rules exist only in docs. Linter errors with remediation instructions produce immediate self-correction.
- Decision: Add `scripts/check_boundaries.py` and `scripts/lint_agent_friendly.py` with remediation-style error messages, enforced via pre-commit hooks and CI.
- Consequences: New rules should be added to scripts/CI, not just documented.

## 2026-03-17 - Separate initializer and coding agent prompts

- Context: Anthropic found that using a different prompt for the first context window (initializer) and subsequent windows (coder) produces better multi-session continuity. The initializer sets up the environment; coding agents do incremental work.
- Decision: Add `prompts/initializer.md`, `prompts/coder.md`, and `prompts/reviewer.md`.
- Consequences: First session of a new feature uses the initializer prompt; all subsequent sessions use the coder prompt.

## 2026-03-17 - Progressive disclosure of context

- Context: HumanLayer found that stuffing all instructions into the system prompt makes agents worse. Skills and on-demand loading solve this.
- Decision: Add `skills/` directory and `docs/architecture/progressive-disclosure.md`. AGENTS.md routes to files; detailed instructions are loaded on demand.
- Consequences: Keep AGENTS.md under 60 lines. Task-specific instructions go in `skills/` or `docs/`.
