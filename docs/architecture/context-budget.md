# Context Window Budget Management

## The constraint

Every agent session has a finite context window. Performance degrades as it fills. This is not a theoretical concern — it is the primary reason long-running agent tasks fail.

## Budget allocation

Think of context as a budget. A typical session has roughly 100-200K tokens. Allocate them deliberately:

| Category | Budget | Notes |
|----------|--------|-------|
| System prompt + AGENTS.md | ~2K | Keep thin |
| Architecture + spec + plan | ~5-10K | Load only the active ones |
| Progress + feature list + decisions | ~2-5K | Always load |
| Code reading | ~30-50K | Read only files relevant to current feature |
| Implementation output | ~30-50K | Code written, tests, commits |
| Tool calls + responses | ~20-40K | Grows with each tool use |
| Reserve for shutdown routine | ~5K | Always keep enough to update artifacts |

## Rules of thumb

### Keep files small

- AGENTS.md: under 60 lines.
- Each doc file: under 200 lines. Split if larger.
- Progress file: keep session log entries to one line each. Archive old entries periodically.
- Feature list: dozens of entries is fine; hundreds is not.

### Load only what you need

The exec plan's "Inputs to load" section defines exactly which files to read. Do not read the entire repository. The reading order in AGENTS.md is a priority list, not a requirement to read everything.

### Recognize context exhaustion

Signs that context is running out:

- Agent starts repeating itself or going in circles.
- Agent forgets instructions from earlier in the session.
- Agent makes mistakes on tasks it handled correctly before.
- Tool call responses are being truncated.

When this happens: **stop, commit, update progress, start a fresh session.**

### Reserve shutdown budget

Never consume the entire context window. Always leave enough room to:

1. Run final tests.
2. Update `artifacts/progress.md`.
3. Update `artifacts/feature-list.json`.
4. Make a clean commit.

If you are at 80% context usage, start the shutdown routine.

## Compaction strategies

### Automatic compaction

Both Claude (Agent SDK) and Codex (agent loop) support automatic compaction — summarizing earlier conversation history to free up space. This happens transparently but is lossy. Important details may be lost.

**Mitigation**: Write important decisions and findings to artifact files *as you discover them*, not just at the end. The files persist; the conversation does not.

### Manual compaction

If you notice context growing large:

1. Commit your current work.
2. Write a detailed progress update.
3. Start a new session that reads the progress file.

A fresh session with a good progress file is more effective than a bloated session.

## File size guidelines

| File type | Target size | Action if exceeded |
|-----------|------------|-------------------|
| AGENTS.md | < 60 lines | Move content to docs/ |
| Product spec | < 200 lines | Split into sub-specs |
| Exec plan | < 150 lines | Split into phases |
| Progress file | < 100 lines | Archive old session logs |
| Architecture docs | < 200 lines each | Split by topic |
| Feature list | < 50 features | Split by module or milestone |

## Reading priority

When context is tight, read files in this order (stop when you have enough):

1. `artifacts/progress.md` — always read first, cheapest way to get current state.
2. `artifacts/feature-list.json` — know what to work on.
3. Active exec plan — know how to do it.
4. Active spec — know why you are doing it.
5. Architecture docs — only if touching boundaries or making design decisions.
6. Quality docs — only if doing review or cleanup.
