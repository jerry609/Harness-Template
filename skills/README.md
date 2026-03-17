# Skills

This directory contains task-specific instruction sets. Agents load a skill only when the current task matches the skill's "When to load" criteria.

## How to use skills

1. Check the "When to load" section of each skill file.
2. If your current task matches, read the skill file before starting work.
3. Follow the skill's instructions alongside the general operating rules in `AGENTS.md`.

## How to create a new skill

1. Copy the template below into a new file: `skills/your-skill.md`.
2. Fill in all sections.
3. Keep it focused — one skill, one type of work.
4. Keep it under 100 lines. If it is longer, split into sub-skills.

## Skill template

```markdown
# Skill: [Name]

## When to load this skill

Describe the conditions under which an agent should read this file.

## Instructions

Step-by-step instructions for this type of work.

## Verification

How to verify this type of work was done correctly.

## Common mistakes

Mistakes agents commonly make with this type of work, and how to avoid them.
```

## Available skills

| Skill | File | Load when |
|-------|------|-----------|
| (Add your skills here) | | |
