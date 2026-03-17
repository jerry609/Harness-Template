# Agent-Friendly Linter Guide

## Core principle

Every linter error message should be a **remediation instruction**, not just a violation report. When an agent hits a lint error, the message itself tells the agent how to fix it.

This is the difference between:

```
# Bad: agent has to guess what to do
ERROR: boundary violation in src/api/handler.py:12

# Good: agent knows exactly what to do
src/api/handler.py:12: BOUNDARY VIOLATION
  Found: from src.infra.db import connection
  Fix: API layer must not import infrastructure directly.
       Define an interface in src/domain/ports.py and inject
       the implementation from the composition root in src/main.py.
```

## Anatomy of a good lint rule

Every rule needs three parts:

1. **Detection**: a pattern (regex, AST check, or file structure check) that identifies the violation.
2. **Explanation**: one sentence saying what is wrong.
3. **Remediation**: exact instructions for the fix, with a code example when possible.

The remediation is the most important part. Without it, agents spin in circles.

## Writing remediation messages

Good remediation messages follow this structure:

```
1. What to do: "Replace X with Y" or "Move X to Z"
2. How to do it: "Example: change 'from a import *' to 'from a import Foo, Bar'"
3. Why (optional): "Wildcard imports make dependencies invisible"
```

Guidelines:

- Use imperative mood: "Replace", "Move", "Add", not "You should replace".
- Include a concrete code example when the fix involves writing code.
- Reference the exact file or location when possible.
- Keep it under 3 sentences. Agents work best with concise instructions.

## Adding rules to the linter

Edit `scripts/lint_agent_friendly.py` and add a `LintRule` to the `RULES` list:

```python
LintRule(
    id="HAR005",
    description="Raw SQL query without parameterization",
    file_glob="src/**/*.py",
    pattern=r'execute\(\s*f["\']',
    remediation=(
        "Use parameterized queries instead of f-strings. "
        "Example: cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,)) "
        "instead of cursor.execute(f'SELECT * FROM users WHERE id = {user_id}')"
    ),
)
```

## Promoting review feedback to lint rules

When the same code review comment appears twice:

1. Write it as a `LintRule` with a clear remediation message.
2. Add it to `scripts/lint_agent_friendly.py`.
3. Add it to CI so it catches future violations automatically.
4. Remove the corresponding item from the review checklist.

This is the **rule promotion** pattern from `docs/quality/cleanup-checklist.md`.

## Boundary checks vs lint rules

Use `scripts/check_boundaries.py` for **architectural constraints** (module A must not import module B).
Use `scripts/lint_agent_friendly.py` for **code-level patterns** (no hardcoded secrets, no wildcard imports).

Both scripts produce remediation-style output that agents can act on directly.
