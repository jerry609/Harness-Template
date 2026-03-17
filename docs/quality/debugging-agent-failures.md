# Debugging Agent Failures

## Core mindset

When an agent struggles, **treat it as an environment bug, not a model limitation.**

OpenAI's harness engineering team stated it plainly: the bottleneck was never the agent's ability to write code, but rather the lack of structure, tools, and feedback mechanisms surrounding it.

## Failure taxonomy

### 1. Agent loops without progress

**Symptom**: Agent repeats the same action, retries the same failing command, or goes in circles.

**Environment fixes**:
- Add a clear stopping condition to the prompt or tool output.
- Make error messages include the exact fix (see `docs/quality/linter-guide.md`).
- Break the task into smaller slices so each has a clear "done" state.
- Check if the agent's context window is full — start a fresh session.

### 2. Agent violates architectural boundaries

**Symptom**: Agent imports from forbidden modules, creates files in wrong directories, or bypasses abstractions.

**Environment fixes**:
- Add the boundary to `scripts/check_boundaries.py` with a remediation message.
- Run boundary checks in pre-commit hooks so violations are caught before commit.
- Make the boundary visible: document it in `docs/architecture/boundaries.md`.

### 3. Agent produces inconsistent output

**Symptom**: Agent's output contradicts previous sessions, or undoes earlier work.

**Environment fixes**:
- Check if `artifacts/progress.md` was updated at the end of the last session.
- Check if the agent is reading the progress file at session start.
- Ensure the coding agent prompt includes the startup routine.
- Clean up stale or contradictory notes in progress.md.

### 4. Agent ignores constraints

**Symptom**: Agent knows the rule (it is in the docs) but does not follow it.

**Environment fixes**:
- Move the rule from documentation to automation (CI, linter, pre-commit hook).
- Rules that exist only in docs will eventually be ignored. Mechanical enforcement wins.
- Check if AGENTS.md or the prompt is too long — constraints at the end get less attention.

### 5. Agent hallucinates APIs or features

**Symptom**: Agent calls functions that do not exist or uses libraries incorrectly.

**Environment fixes**:
- Pin dependency versions and include them in the environment setup.
- Prefer well-documented, training-data-rich libraries (see `docs/architecture/tech-selection.md`).
- Add type stubs or interface definitions so the agent can verify its calls.
- Include a smoke test that catches import errors early.

### 6. Agent produces working but wrong code

**Symptom**: Tests pass but the feature does not match the spec.

**Environment fixes**:
- Write acceptance criteria as testable assertions, not prose.
- Use the test-first pattern (test agent writes tests, coding agent implements).
- Have a reviewer agent check output against the spec (see `prompts/reviewer.md`).
- Add eval tasks that verify end-state, not just "code runs."

### 7. Agent gets stuck on setup or environment issues

**Symptom**: Agent spends most of the session fighting dependencies, permissions, or configuration.

**Environment fixes**:
- Improve `scripts/init.sh` to handle all setup automatically.
- Add a smoke test (`scripts/smoke.sh`) that verifies the environment before coding starts.
- Document prerequisites in the exec plan's "Inputs to load" section.
- Use containerized environments when the setup is complex.

## Diagnostic flowchart

```
Agent failed
  │
  ├─ Is it looping? → Add stopping conditions, check context fullness
  │
  ├─ Is it violating rules? → Move rule to automation (CI/linter/hook)
  │
  ├─ Is it contradicting prior work? → Fix progress file, check startup routine
  │
  ├─ Is it ignoring docs? → Docs alone are not enough, enforce mechanically
  │
  ├─ Is it hallucinating? → Pin deps, use mature libraries, add type checks
  │
  ├─ Is it wrong but passing tests? → Fix tests/specs, add reviewer agent
  │
  └─ Is it stuck on setup? → Fix init scripts, add smoke test
```

## The rule promotion ladder

When the same failure happens more than once, promote the fix:

```
1. Fix it manually
2. Document it in a checklist
3. Add it to a script
4. Add it to CI
5. Add it to pre-commit hooks
```

Each step makes the fix more automatic and harder to skip.
