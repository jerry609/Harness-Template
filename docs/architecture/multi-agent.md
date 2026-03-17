# Multi-Agent Patterns

## Why multiple agents

A single agent session has two limitations:

1. **Context window**: one session cannot hold an entire large project.
2. **Self-bias**: an agent reviewing its own code tends to overlook the same mistakes it made writing it.

Multi-agent patterns solve both problems by splitting work across independent sessions.

## Pattern 1: Writer / Reviewer

The most impactful pattern. Use one agent to write code, then a **separate agent with fresh context** to review it.

```
[Writer Agent]
  └─ Writes code, creates PR
        ↓
[Reviewer Agent]  (fresh context, no memory of writing)
  └─ Reviews the PR diff against spec and architecture
  └─ Posts review comments with specific fix instructions
        ↓
[Writer Agent]
  └─ Reads review comments, applies fixes
        ↓
[Reviewer Agent]
  └─ Re-reviews, approves or requests more changes
```

### Why it works

- The reviewer starts with a **clean context window**, so it actually reads the diff instead of assuming it is correct.
- The reviewer can be given a **stricter prompt** focused on catching common mistakes.
- Agents are less biased toward code they did not write.

### Reviewer agent prompt

See `prompts/reviewer.md` for a ready-to-use reviewer prompt.

## Pattern 2: Parallel Feature Agents

When features are independent, run multiple coding agents in parallel on different features.

```
[Agent A] ──→ Feature 1 ──→ PR #1
[Agent B] ──→ Feature 2 ──→ PR #2
[Agent C] ──→ Feature 3 ──→ PR #3
```

### Prerequisites for parallel agents

- Features must be **independent** (no shared files being modified).
- Each agent works on a **separate branch**.
- Boundary rules and CI catch integration conflicts at merge time.
- `artifacts/feature-list.json` tracks ownership to prevent double-work.

### Ownership tracking

Add an `owner` field to features in `feature-list.json`:

```json
{
  "id": "auth-login",
  "title": "Login endpoint",
  "status": "in_progress",
  "owner": "agent-A"
}
```

## Pattern 3: Test Writer / Implementation Writer

A variation of writer/reviewer where the first agent writes tests, then a second agent writes implementation to pass them.

```
[Test Agent]
  └─ Reads spec → Writes failing tests → Commits
        ↓
[Implementation Agent]
  └─ Reads tests → Writes code until tests pass → Commits
```

### Why it works

- Tests become an **unambiguous specification**.
- The implementation agent has a clear "definition of done": all tests green.
- Neither agent is biased by the other's approach.

## Pattern 4: Agent-to-Agent Code Review Loop

For high-throughput teams, automate the entire review cycle:

1. Writer agent creates a PR.
2. Reviewer agent is triggered automatically (via CI or webhook).
3. Reviewer posts comments.
4. Writer agent reads comments and pushes fixes.
5. Reviewer re-reviews.
6. After approval, PR is merged (or escalated to human if reviewer is unsatisfied after 2 rounds).

### Escalation rules

Escalate to a human when:

- The reviewer agent rejects the PR after 2 review rounds.
- The change touches security-sensitive code.
- The change modifies architectural boundaries.
- The agents disagree on a design tradeoff.

## When NOT to use multi-agent patterns

- **Small tasks**: a single session can handle a bug fix or small feature. Adding agents adds overhead.
- **Tightly coupled changes**: if every feature touches the same files, parallel agents will create merge conflicts.
- **Early exploration**: when you are still figuring out what to build, a single agent conversation is faster.

## Implementing in practice

### With Claude Code

Use Claude Code's built-in team features:
- Spawn writer and reviewer as separate agents.
- Use task lists for coordination.
- Use messaging for handoff between agents.

### With Codex

- Run separate Codex sessions on different branches.
- Use GitHub PR reviews as the coordination layer.
- Set up CI to trigger reviewer agents on PR creation.

### With any agent

- Use Git branches as isolation boundaries.
- Use `artifacts/feature-list.json` ownership to prevent conflicts.
- Use PR templates (`prompts/reviewer.md`) to structure reviews.
