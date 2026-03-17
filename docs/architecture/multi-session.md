# Multi-Session Workflow

## The problem

Complex tasks cannot be completed in a single context window. When an agent starts a new session, it has **zero memory** of previous sessions. Without structured handoff, work is lost, duplicated, or contradicted.

## The solution: initializer + coding agent pattern

Use two distinct prompts for two phases of work:

### Phase 1: Initialization (one session)

The initializer agent (`prompts/initializer.md`) runs once to:

- Break the spec into a granular feature list (all marked "backlog").
- Create the execution plan with session-sized work slices.
- Set up the development environment.
- Create stub tests for the first features.
- Write the initial progress file.

### Phase 2: Incremental coding (many sessions)

Each coding agent session (`prompts/coder.md`):

1. Reads the progress file and feature list to understand current state.
2. Picks up the next feature.
3. Implements, tests, and verifies.
4. Updates progress and feature status.
5. Commits and stops cleanly.

```
Session 0: Initializer
  └─ Creates: feature-list.json, progress.md, exec-plan, stub tests, environment

Session 1: Coding Agent
  └─ Reads progress → Implements feature 1 → Updates progress → Commits

Session 2: Coding Agent
  └─ Reads progress → Implements feature 2 → Updates progress → Commits

  ...

Session N: Coding Agent
  └─ Reads progress → All features done → Final cleanup → Done
```

## External artifacts as memory

The agent's memory lives in these files:

| File | Purpose |
|------|---------|
| `artifacts/progress.md` | What happened, what to do next, what is blocked |
| `artifacts/feature-list.json` | Status of every feature (backlog → in_progress → done) |
| `artifacts/decisions.md` | Durable tradeoffs and their reasoning |
| `docs/exec-plans/*.md` | The step-by-step plan |
| Git history | What changed and when |

## Context window budget

Each session has a limited context window. Manage it:

- Load only the files listed in the exec plan's "Inputs to load" section.
- Do not read the entire codebase. Read what you need for the current feature.
- If context is running low, commit progress and start a fresh session.
- The progress file is cheaper to read than the full conversation history.

## When to re-initialize

Re-run the initializer agent when:

- A major scope change invalidates the current feature list.
- The project has pivoted and the execution plan no longer applies.
- More than half the features need to be redefined.

Do NOT re-initialize for:

- Adding a few features (just edit `feature-list.json` directly).
- Changing implementation details within existing features.
- Bug fixes or small adjustments.

## Anti-patterns

| Anti-pattern | Fix |
|-------------|-----|
| Agent tries to build everything in one session | Break into features, enforce one-per-session |
| Agent loses context mid-task | Write progress before context fills up |
| Agent contradicts previous session's work | Read progress.md and git log before starting |
| Agent skips verification | Include verification in the coding agent prompt |
| Progress file is vague ("made some progress") | Require specific next action and test results |
