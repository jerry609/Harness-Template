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
3. Create your first real work item with `python scripts/init_task.py my-feature "My Feature"`.
4. Replace the sample entries in `artifacts/feature-list.json` and `artifacts/progress.md`.
5. Extend `scripts/validate_artifacts.py` and `.github/workflows/ci.yml` with project-specific rules.

## What this template includes

- A thin `AGENTS.md` with reading order, operating rules, and done criteria.
- `docs/` folders for architecture, product specs, execution plans, quality rules, and references.
- `artifacts/` files for progress tracking, feature status, and decisions.
- `evals/` scaffolding for tasks, graders, and outcome-oriented verification.
- `scripts/` helpers to create new work items and validate the repository shape.
- A simple GitHub Actions workflow to enforce the baseline structure.

## Repository layout

```text
.
|-- .github/
|   |-- PULL_REQUEST_TEMPLATE.md
|   `-- workflows/ci.yml
|-- .gitignore
|-- AGENTS.md
|-- README.md
|-- artifacts/
|   |-- decisions.md
|   |-- feature-list.json
|   `-- progress.md
|-- docs/
|   |-- architecture/index.md
|   |-- exec-plans/TEMPLATE.md
|   |-- product-specs/TEMPLATE.md
|   |-- quality/
|   |   |-- cleanup-checklist.md
|   |   |-- golden-principles.md
|   |   `-- quality-score.md
|   `-- references/agent-engineering-reading-list.md
|-- evals/
|   |-- README.md
|   |-- graders/README.md
|   `-- tasks/sample-task.md
`-- scripts/
    |-- init.ps1
    |-- init.sh
    |-- init_task.py
    |-- smoke.ps1
    |-- smoke.sh
    `-- validate_artifacts.py
```

## Operating loop

1. Start from a product spec, not a vague prompt.
2. Create an execution plan that points to the exact context files to load.
3. Work on one feature or bug per session.
4. Verify with evals, smoke checks, or real environment feedback.
5. Update progress, feature status, and decisions before you stop.
6. Convert repeated review feedback into docs, scripts, or CI checks.

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
  - Template impact: `AGENTS.md` stays thin, core knowledge moves into `docs/`, and rules are pushed toward scripts and CI.
- [From model to agent: Equipping the Responses API with a computer environment](https://openai.com/index/equip-responses-api-computer-environment) - March 11, 2026
  - Template impact: `scripts/`, eval scaffolding, and explicit environment validation are first-class parts of the repo.
- [Unrolling the Codex agent loop](https://openai.com/index/unrolling-the-codex-agent-loop/) - January 23, 2026
  - Template impact: work is structured around small loops, artifact updates, and stable handoff points.

### Anthropic

- [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) - September 29, 2025
  - Template impact: context is organized as small, discoverable files with explicit reading order.
- [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) - November 26, 2025
  - Template impact: `artifacts/progress.md`, `artifacts/feature-list.json`, and small-session discipline are built in.
- [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) - January 9, 2026
  - Template impact: `evals/` is organized around tasks, trials, graders, transcripts, and outcomes.
- [Writing effective tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents) - September 11, 2025
  - Template impact: helper scripts use clear names, structured inputs, and explicit outputs.
- [Building effective agents](https://www.anthropic.com/research/building-effective-agents/) - December 19, 2024
  - Template impact: the template starts with simple workflows and only adds autonomy where it earns its keep.

## Recommended first customizations

- Replace the sample feature in `artifacts/feature-list.json` with your first real feature.
- Tighten `scripts/validate_artifacts.py` so it enforces your project-specific rules.
- Add project-specific evals under `evals/tasks/`.
- Extend `.github/workflows/ci.yml` with lint, tests, and any structure checks you care about.
- Move any recurring review comments into `docs/quality/` or CI.

## Suggested next layers

Once this template is in use, add the following in order:

1. Project-specific lint and test commands.
2. Boundary checks for your module or service layers.
3. Outcome-based eval tasks for the highest-value workflows.
4. Automated cleanup jobs or recurring cleanup PRs.
