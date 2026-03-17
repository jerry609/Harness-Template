# Boundary Rules

Define your module boundaries here. The goal is to make dependency violations **mechanically detectable** so agents get instant feedback instead of silent drift.

## How to define a boundary

Each boundary rule has three parts:

1. **Module**: the directory or package being protected.
2. **Allowed imports**: what the module is permitted to depend on.
3. **Forbidden imports**: what the module must never touch.

## Example rules

```yaml
# boundaries.yml — machine-readable boundary definitions
boundaries:
  - module: "src/api/"
    allowed:
      - "src/domain/"
      - "src/shared/"
    forbidden:
      - "src/infra/"
      - "src/cli/"
    reason: "API layer depends on domain, never on infrastructure directly."

  - module: "src/domain/"
    allowed:
      - "src/shared/"
    forbidden:
      - "src/api/"
      - "src/infra/"
      - "src/cli/"
    reason: "Domain is the innermost layer. It must not import anything outside shared utilities."

  - module: "src/infra/"
    allowed:
      - "src/domain/"
      - "src/shared/"
    forbidden:
      - "src/api/"
    reason: "Infrastructure implements domain interfaces. It never imports the API layer."
```

## Adding a boundary

1. Describe the rule in this file.
2. Add the machine-readable version to `boundaries.yml` (or inline in `scripts/check_boundaries.py`).
3. Run `python scripts/check_boundaries.py` locally.
4. CI enforces boundaries on every push and pull request.

## Why mechanical enforcement matters

OpenAI's harness engineering team found that agents work best inside **strict, enforced boundaries**. Written guidelines alone are not enough — agents will drift. When a boundary violation produces an error message with a clear fix instruction, the agent self-corrects immediately.

## Guidance for writing boundary rules

- Start with the obvious: domain must not import infrastructure.
- Add boundaries only when a real violation has occurred or is likely.
- Keep the rule set small. A dozen rules is better than a hundred.
- Every rule should include a `reason` so agents (and humans) understand the intent.
- When you remove a boundary, record why in `artifacts/decisions.md`.
