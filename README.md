# Routa Harness Template

A practical starter template for agent-first engineering, extracted from Routa's workflow and aligned with recent OpenAI and Anthropic engineering articles.

This template is intentionally lightweight:

- `AGENTS.md` is a router, not an encyclopedia.
- Knowledge lives in versioned files inside the repo.
- Architecture and quality rules are meant to become mechanical checks.
- Sessions are small, explicit, and leave a clean handoff.
- Evals grade outcomes, not just agent narration.

## Use this template

1. Copy the contents of this directory into a new repository root.
2. Read `AGENTS.md` and `docs/architecture/index.md`.
3. Install pre-commit hooks: `pip install pre-commit && pre-commit install`.
4. Create your first real work item with `python scripts/init_task.py my-feature "My Feature"`.
5. Replace the sample entries in `artifacts/feature-list.json` and `artifacts/progress.md`.
6. Customize boundary rules in `scripts/check_boundaries.py` or create a `boundaries.yml`.
7. Add project-specific lint rules to `scripts/lint_agent_friendly.py`.
8. Extend `.github/workflows/ci.yml` with project-specific checks.

## What this template includes

- A thin `AGENTS.md` with reading order, on-demand context loading, operating rules, and done criteria.
- `docs/` folders for architecture, product specs, execution plans, quality rules, and references.
- `artifacts/` files for progress tracking, feature status, and decisions.
- `evals/` scaffolding for tasks, graders, and outcome-oriented verification.
- `prompts/` agent-specific prompts: initializer, coder, and reviewer.
- `skills/` on-demand instruction sets for specialized tasks (progressive disclosure).
- `scripts/` helpers: task creation, artifact validation, boundary checks, and agent-friendly linting.
- `.pre-commit-config.yaml` for pre-commit hook enforcement.
- A GitHub Actions workflow to enforce structure, boundaries, and lint rules.

## Repository layout

```text
.
|-- .github/
|   |-- PULL_REQUEST_TEMPLATE.md
|   `-- workflows/ci.yml
|-- .gitignore
|-- .pre-commit-config.yaml
|-- AGENTS.md
|-- README.md
|-- artifacts/
|   |-- decisions.md
|   |-- feature-list.json
|   `-- progress.md
|-- docs/
|   |-- architecture/
|   |   |-- boundaries.md
|   |   |-- context-budget.md
|   |   |-- index.md
|   |   |-- multi-agent.md
|   |   |-- multi-session.md
|   |   |-- progressive-disclosure.md
|   |   `-- tech-selection.md
|   |-- exec-plans/TEMPLATE.md
|   |-- product-specs/TEMPLATE.md
|   |-- quality/
|   |   |-- cleanup-checklist.md
|   |   |-- debugging-agent-failures.md
|   |   |-- golden-principles.md
|   |   |-- linter-guide.md
|   |   `-- quality-score.md
|   `-- references/agent-engineering-reading-list.md
|-- evals/
|   |-- README.md
|   |-- graders/README.md
|   `-- tasks/sample-task.md
|-- prompts/
|   |-- coder.md
|   |-- initializer.md
|   `-- reviewer.md
|-- scripts/
|   |-- check_boundaries.py
|   |-- init.ps1
|   |-- init.sh
|   |-- init_task.py
|   |-- lint_agent_friendly.py
|   |-- pre-commit-validate.sh
|   |-- smoke.ps1
|   |-- smoke.sh
|   `-- validate_artifacts.py
`-- skills/
    `-- README.md
```

## Operating loop

1. Start from a product spec, not a vague prompt.
2. Run the initializer agent (`prompts/initializer.md`) for the first session of a new feature.
3. Use the coding agent (`prompts/coder.md`) for all subsequent sessions.
4. Work on one feature or bug per session.
5. Verify with evals, smoke checks, boundary checks, and linting.
6. Update progress, feature status, and decisions before you stop.
7. Use the reviewer agent (`prompts/reviewer.md`) on PRs before merging.
8. Convert repeated review feedback into docs, scripts, or CI checks.

## Garbage collection loop

This template treats cleanup as part of delivery, not an afterthought.

- Minor cleanup: remove dead code, stale notes, and temporary hacks during each session.
- Major cleanup: run periodic refactors for duplicated abstractions, stale docs, and broken boundaries.
- Rule promotion: when the same failure happens twice, encode it into a checklist, script, or CI rule.

See `docs/quality/cleanup-checklist.md` and `docs/quality/quality-score.md`.

## Reference implementations

- [phodal/routa](https://github.com/phodal/routa) - practical multi-agent coordination platform with explicit `AGENTS.md`, fitness functions, specialist roles, and issue feedback loops.
- [openai/codex](https://github.com/openai/codex) - a strong reference for repo organization, `AGENTS.md`, skills, and agent-friendly structure.
- [SWE-agent/SWE-agent](https://github.com/SWE-agent/SWE-agent) - useful for issue-to-fix-to-verification workflows.
- [GoogleCloudPlatform/agent-starter-pack](https://github.com/GoogleCloudPlatform/agent-starter-pack) - helpful when you want production starter layers such as CI/CD and observability.

## How the references shape this template

The following references were verified on March 17, 2026 and are included both here and in `docs/references/agent-engineering-reading-list.md`.

### OpenAI

- [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering) - February 11, 2026
  - Template impact: `AGENTS.md` stays thin, core knowledge moves into `docs/`, rules are enforced by `scripts/check_boundaries.py` and `scripts/lint_agent_friendly.py`. Linter errors are remediation instructions. Agent failures are treated as environment bugs.
- [From model to agent: Equipping the Responses API with a computer environment](https://openai.com/index/equip-responses-api-computer-environment) - March 11, 2026
  - Template impact: `scripts/`, eval scaffolding, and explicit environment validation are first-class parts of the repo.
- [Unrolling the Codex agent loop](https://openai.com/index/unrolling-the-codex-agent-loop/) - January 23, 2026
  - Template impact: work is structured around small loops, artifact updates, and stable handoff points.

### Anthropic

- [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) - September 29, 2025
  - Template impact: context is organized as small, discoverable files with explicit reading order.
- [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) - November 26, 2025
  - Template impact: `artifacts/progress.md`, `artifacts/feature-list.json`, small-session discipline, and the initializer/coder agent split (`prompts/`) are built in.
- [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) - January 9, 2026
  - Template impact: `evals/` is organized around tasks, trials, graders, transcripts, and outcomes.
- [Writing effective tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents) - September 11, 2025
  - Template impact: helper scripts use clear names, structured inputs, and explicit outputs.
- [Building effective agents](https://www.anthropic.com/research/building-effective-agents/) - December 19, 2024
  - Template impact: the template starts with simple workflows and only adds autonomy where it earns its keep.

## Recommended first customizations

- Replace the sample feature in `artifacts/feature-list.json` with your first real feature.
- Add boundary rules to `scripts/check_boundaries.py` or `boundaries.yml` for your project's module structure.
- Add project-specific lint rules to `scripts/lint_agent_friendly.py` with remediation messages.
- Customize `prompts/initializer.md` and `prompts/coder.md` for your project's workflow.
- Add project-specific evals under `evals/tasks/`.
- Create skills under `skills/` for recurring specialized tasks.
- Move any recurring review comments into `docs/quality/` or CI.

## Suggested next layers

Once this template is in use, add the following in order:

1. Project-specific lint and test commands.
2. Boundary checks for your module or service layers.
3. Agent-to-agent code review automation (see `docs/architecture/multi-agent.md`).
4. Outcome-based eval tasks for the highest-value workflows.
5. Parallel agent workflows for independent features.
6. Automated cleanup jobs or recurring cleanup PRs.
