## Goal

Link the spec and describe the intended outcome.

## Plan

Link the execution plan and describe the slice completed in this PR.

## Verification

- [ ] Outcome-oriented verification completed
- [ ] `python scripts/validate_artifacts.py` passed
- [ ] `python scripts/check_boundaries.py` passed
- [ ] `python scripts/lint_agent_friendly.py` passed
- [ ] Relevant docs updated

## Agent review checklist

- [ ] Code respects module boundaries defined in `docs/architecture/boundaries.md`
- [ ] No hardcoded secrets or credentials
- [ ] Error messages include remediation instructions
- [ ] Tests verify behavior, not just that code runs
- [ ] Changes are scoped to one feature / one coherent slice

## Cleanup

- [ ] Temporary code removed
- [ ] `artifacts/progress.md` updated
- [ ] `artifacts/feature-list.json` updated
- [ ] Durable decisions captured if needed