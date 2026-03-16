# Cleanup Checklist

Treat cleanup like garbage collection for agent-generated work.

## Every session

- Remove temporary debugging code.
- Remove dead files or dead branches introduced by the change.
- Update stale progress notes.
- Confirm the feature status is still correct.
- Make sure docs and verification match the latest behavior.

## Weekly cleanup

- Merge or remove duplicated helpers.
- Tighten rules that were only enforced in review.
- Archive or rewrite stale docs.
- Remove obsolete plans that no longer reflect reality.
- Add eval tasks for recent production or user-facing failures.

## Rule promotion

If the same issue appears more than once, upgrade it:

1. Add it to a checklist.
2. Add it to a script.
3. Add it to CI.

## Common garbage to collect

- dead code
- stale documentation
- duplicate abstractions
- misleading file names
- oversized files with mixed responsibilities
- temporary workarounds that became permanent
- evals that check the wrong thing