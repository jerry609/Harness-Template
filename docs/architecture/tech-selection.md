# Technology Selection for Agent-Friendly Projects

## The principle: boring technology wins

OpenAI's harness engineering experience showed that agents perform significantly better with **mature, well-documented, widely-used technologies** compared to cutting-edge frameworks with sparse documentation.

This is not about technical conservatism — it is about training data coverage. Models have seen millions of examples of Express.js, Django, Spring Boot, and PostgreSQL. They have seen far fewer examples of last month's new framework.

## Selection criteria

When choosing a technology for an agent-assisted project, evaluate:

| Factor | Prefer | Avoid |
|--------|--------|-------|
| Training data coverage | Large, mature ecosystem | New framework with few examples |
| Documentation | Comprehensive, up-to-date docs | "Read the source code" |
| API surface | Small, composable, stable | Large surface with frequent breaking changes |
| CLI availability | Strong CLI tools | GUI-only configuration |
| Error messages | Clear, actionable errors | Cryptic error codes |
| Community | Large Stack Overflow presence | Niche community |

## CLI over MCP

When a capability is available both as a **CLI tool** and as an **MCP server**:

- **Prefer CLI** if the tool is well-represented in training data (git, docker, kubectl, psql, curl, jq).
- **Prefer MCP** only when the CLI does not exist or is poorly documented.

Why: CLI tools are composable (pipe, grep, jq), well-represented in training data, and do not require running a server. Agents already know how to use them.

## When reimplementation is cheaper

OpenAI found that sometimes it is cheaper to **reimplement functionality** than to fight opaque upstream behavior from a dependency.

Consider reimplementation when:
- The dependency solves a small problem but brings a large, complex API.
- The dependency has undocumented behavior that agents cannot predict.
- The dependency's error messages are not actionable.
- The dependency changes frequently, breaking agent-generated code.

Do NOT reimplement when:
- The dependency solves a complex, well-defined problem (crypto, compression, database drivers).
- The dependency is a de facto standard with excellent documentation.
- The reimplementation would be larger than the dependency itself.

## Practical guidelines

### For web projects
- **Backend**: Express.js, Django, Flask, Spring Boot — not the framework released last month.
- **Database**: PostgreSQL, SQLite, MySQL — not a new distributed database with 20 pages of docs.
- **Frontend**: React, Vue — stable versions, not canary/experimental APIs.

### For infrastructure
- **Containers**: Docker, standard Dockerfiles — not exotic build systems.
- **CI/CD**: GitHub Actions, standard YAML — not custom CI frameworks.
- **IaC**: Terraform, Pulumi — with well-documented providers.

### For scripting
- **Languages**: Python, Bash, Node.js — agents have extensive training data.
- **Package managers**: pip, npm, go modules — standard tools, not wrappers.

## Decision record

When you choose a technology, record the decision in `artifacts/decisions.md` with:
- What you chose and what you rejected.
- Why (training data coverage, documentation quality, API stability).
- What to do if the choice needs to change later.
