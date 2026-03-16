# Agent Engineering Reading List

These references were verified on March 17, 2026 and directly informed this template.

## OpenAI

- [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering) - February 11, 2026
  - Why it matters: argues that `AGENTS.md` should route to repo-local knowledge instead of duplicating it.
  - Template mapping: `AGENTS.md`, `docs/architecture/index.md`, `.github/workflows/ci.yml`
- [From model to agent: Equipping the Responses API with a computer environment](https://openai.com/index/equip-responses-api-computer-environment) - March 11, 2026
  - Why it matters: shows that tools, filesystems, and execution environments are part of the product surface.
  - Template mapping: `scripts/`, `evals/`, validation workflow
- [Unrolling the Codex agent loop](https://openai.com/index/unrolling-the-codex-agent-loop/) - January 23, 2026
  - Why it matters: clarifies how agent loops consume context and why handoff artifacts matter.
  - Template mapping: `artifacts/progress.md`, small-session workflow

## Anthropic

- [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) - September 29, 2025
  - Why it matters: context is scarce, so shape it into high-signal, discoverable files.
  - Template mapping: reading order, small docs, stable paths
- [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) - November 26, 2025
  - Why it matters: long tasks need progress files, feature lists, and clean stopping points.
  - Template mapping: `artifacts/feature-list.json`, `artifacts/progress.md`
- [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) - January 9, 2026
  - Why it matters: evals should distinguish tasks, trials, transcripts, graders, and outcomes.
  - Template mapping: `evals/README.md`, `evals/tasks/`, `evals/graders/`
- [Writing effective tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents) - September 11, 2025
  - Why it matters: tool design is interface design for agents.
  - Template mapping: `scripts/init_task.py`, `scripts/validate_artifacts.py`
- [Building effective agents](https://www.anthropic.com/research/building-effective-agents/) - December 19, 2024
  - Why it matters: start with simple workflows and only add autonomy when needed.
  - Template mapping: repo structure stays simple and explicit by default

## Practical reference implementations

- [Routa repository](https://github.com/phodal/routa)
  - Why it matters: shows harness engineering in a real multi-agent product, including specialist roles, issue feedback loops, and fitness checks.
  - Template mapping: `AGENTS.md`, `docs/quality/`, `artifacts/`, `.github/`
- [Routa harness engineering section](../../README.md)
  - Why it matters: explains how the product applies system readability, defense mechanisms, and automated feedback in practice.
  - Template mapping: repo-level operating model and guardrail mindset
- [OpenAI Codex repository](https://github.com/openai/codex)
  - Why it matters: useful reference for repository structure, skills, and a thin routing file.
  - Template mapping: `AGENTS.md`, discoverable repo layout
- [SWE-agent](https://github.com/SWE-agent/SWE-agent)
  - Why it matters: strong reference for issue-driven execution and outcome validation.
  - Template mapping: `evals/`, task workflow, verification discipline
