# Progressive Disclosure

## The problem

Stuffing every instruction, rule, and tool into the system prompt makes agents **worse**, not better. Each additional instruction competes for attention in the context window. Instructions at the end get less weight. Agents start ignoring or contradicting rules when there are too many.

## The solution: load context on demand

Only give the agent the instructions, knowledge, and tools it needs for the **current task**. Everything else stays in files, ready to be loaded when needed.

## How this template implements progressive disclosure

### Layer 1: Always loaded (system prompt / AGENTS.md)

- Reading order (where to find things).
- Operating rules (how to work).
- Definition of done (when to stop).

This is the thin router. Under 60 lines.

### Layer 2: Loaded per session (exec plan "Inputs to load")

- The active product spec.
- The active execution plan.
- Architecture docs relevant to the current feature.
- Progress file and feature list.

The exec plan template includes an "Inputs to load" section that explicitly lists which files the coding agent should read. This prevents the agent from loading irrelevant context.

### Layer 3: Loaded on demand (skills and reference docs)

- Quality rules (only when doing review or cleanup).
- Technology selection guide (only when choosing a dependency).
- Debugging guide (only when an agent is failing).
- Domain-specific skills (only when the task requires them).

These live in `docs/` and `skills/` and are loaded only when the agent or prompt explicitly requests them.

## Skills directory

The `skills/` directory contains **task-specific instruction sets** that agents load when they need specialized knowledge. Each skill is a markdown file with focused instructions for one type of work.

### Structure of a skill file

```markdown
# Skill: Database Migration

## When to load this skill
Load this skill when the current task involves creating, modifying,
or rolling back database schema changes.

## Instructions
[Specific, focused instructions for this type of work]

## Verification
[How to verify this type of work was done correctly]

## Common mistakes
[Mistakes agents commonly make with this type of work]
```

### Example skills

| Skill | Load when |
|-------|-----------|
| `skills/database-migration.md` | Task involves schema changes |
| `skills/api-design.md` | Task involves creating or modifying API endpoints |
| `skills/security-review.md` | Task involves auth, crypto, or user data |
| `skills/performance-optimization.md` | Task involves profiling or optimization |
| `skills/frontend-component.md` | Task involves UI component creation |

### How agents use skills

In the coding agent prompt, skills are loaded via a simple instruction:

```
If your current task involves [topic], read `skills/[topic].md` before proceeding.
```

The agent decides whether to load the skill based on the task description. This is progressive disclosure — the agent only gets specialized instructions when it needs them.

## Anti-patterns

| Anti-pattern | Fix |
|-------------|-----|
| Everything in AGENTS.md | Move to docs/ and skills/, keep AGENTS.md as router |
| 20 rules in system prompt | Keep 5-7 core rules, move rest to quality docs |
| All tools always available | Group tools by task type, load on demand |
| Loading every doc at session start | Use exec plan "Inputs to load" as whitelist |
| Skill files that are 500 lines | Split into sub-skills or extract to separate docs |
