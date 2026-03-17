# Architecture Index

This repository is organized for agent legibility first.

## Source-of-truth model

- `docs/product-specs/` answers what should be built and why.
- `docs/exec-plans/` answers how the current change will be executed.
- `docs/architecture/boundaries.md` answers what dependencies are allowed.
- `docs/architecture/multi-session.md` answers how to work across context windows.
- `docs/architecture/multi-agent.md` answers how to coordinate multiple agents.
- `docs/architecture/context-budget.md` answers how to manage context window limits.
- `docs/architecture/tech-selection.md` answers how to choose technologies.
- `docs/architecture/progressive-disclosure.md` answers when to load what context.
- `artifacts/feature-list.json` answers what state each feature is in.
- `artifacts/progress.md` answers what happened most recently.
- `artifacts/decisions.md` answers why durable tradeoffs were made.
- `evals/` answers whether the system actually worked.
- `scripts/` provides narrow tools with stable, explicit behavior.
- `prompts/` provides agent-specific prompts for different session types.
- `skills/` provides task-specific instructions loaded on demand.
- `AGENTS.md` only routes the agent to the right files.

## Boundary rules

- Do not store core project knowledge only in `AGENTS.md`.
- Do not mix product requirements into execution plans.
- Do not treat a passing narration as success; verify through outcomes.
- Do not leave long-running work without a progress update and next action.
- Do not keep repeated quality rules only in human review comments.

## Dependency flow

Use this flow whenever possible:

`product spec -> execution plan -> implementation -> verification -> progress update -> cleanup`

## Mechanical checks to add in a real project

Add these gradually as your project matures:

- lint and formatting checks
- agent-friendly linter with remediation messages (`scripts/lint_agent_friendly.py`)
- module boundary enforcement (`scripts/check_boundaries.py`)
- pre-commit hooks (`.pre-commit-config.yaml`)
- unit and integration tests
- dependency boundary tests
- schema validation at system boundaries
- file size or ownership checks
- documentation freshness checks
- security and reliability checks

## Design goal

The design goal is not maximum cleverness. The design goal is a repository that a new agent can inspect, understand, modify, and verify with minimal hidden context.