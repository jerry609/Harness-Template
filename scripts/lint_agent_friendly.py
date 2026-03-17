#!/usr/bin/env python3
"""Agent-friendly linter with remediation-style error messages.

Every error message tells the agent exactly how to fix the problem.
This is the key insight from OpenAI's harness engineering: linter output
should teach the agent while it works.

Usage:
    python scripts/lint_agent_friendly.py
    python scripts/lint_agent_friendly.py --path src/

Customize RULES below with your project-specific patterns.
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


@dataclass
class LintRule:
    """A single lint rule with remediation instructions."""

    id: str
    description: str
    file_glob: str
    pattern: str  # regex to detect the violation
    remediation: str  # exact instructions for the agent to fix it
    severity: str = "error"  # error | warning


# ---------------------------------------------------------------------------
# Define your project-specific rules here.
# The remediation field is the most important part — it tells the agent
# exactly what to do instead of just flagging the problem.
# ---------------------------------------------------------------------------
RULES: list[LintRule] = [
    LintRule(
        id="HAR001",
        description="Hardcoded secret or credential",
        file_glob="**/*.py",
        pattern=r"""(?i)(password|secret|api_key|token)\s*=\s*["'][^"']+["']""",
        remediation=(
            "Do not hardcode secrets. "
            "Move the value to an environment variable and read it with os.environ.get(). "
            "Example: api_key = os.environ.get('API_KEY')"
        ),
    ),
    LintRule(
        id="HAR002",
        description="TODO without owner or issue reference",
        file_glob="**/*.py",
        pattern=r"#\s*TODO(?!\s*\()",
        remediation=(
            "Add an owner or issue reference to the TODO. "
            "Format: # TODO(username): description or # TODO(#123): description"
        ),
        severity="warning",
    ),
    LintRule(
        id="HAR003",
        description="Wildcard import",
        file_glob="**/*.py",
        pattern=r"^from\s+\S+\s+import\s+\*",
        remediation=(
            "Replace the wildcard import with explicit names. "
            "Wildcard imports pollute the namespace and make dependencies invisible. "
            "Example: change 'from module import *' to 'from module import ClassA, func_b'"
        ),
    ),
    LintRule(
        id="HAR004",
        description="Print statement in production code",
        file_glob="src/**/*.py",
        pattern=r"^\s*print\(",
        remediation=(
            "Replace print() with a logger call. "
            "Example: logger.info('message') instead of print('message'). "
            "Import the logger with: import logging; logger = logging.getLogger(__name__)"
        ),
    ),
    # -----------------------------------------------------------------------
    # Add your own rules below. Focus on the remediation message.
    # A good remediation message:
    # 1. Says what is wrong (one sentence).
    # 2. Says exactly what to do instead (with a code example if possible).
    # 3. Explains why (one sentence, optional).
    # -----------------------------------------------------------------------
]


def run_rules(
    rules: list[LintRule], search_root: Path
) -> list[tuple[LintRule, Path, int, str]]:
    violations: list[tuple[LintRule, Path, int, str]] = []
    for rule in rules:
        compiled = re.compile(rule.pattern)
        for filepath in search_root.glob(rule.file_glob):
            if not filepath.is_file():
                continue
            # Skip hidden directories and common non-source paths
            parts = filepath.relative_to(search_root).parts
            if any(p.startswith(".") or p in ("node_modules", "__pycache__", "venv") for p in parts):
                continue
            try:
                lines = filepath.read_text(encoding="utf-8").splitlines()
            except (OSError, UnicodeDecodeError):
                continue
            for line_num, line in enumerate(lines, start=1):
                if compiled.search(line):
                    violations.append((rule, filepath, line_num, line))
    return violations


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Agent-friendly linter with remediation messages."
    )
    parser.add_argument(
        "--path",
        type=Path,
        default=ROOT,
        help="Directory to lint (default: repository root).",
    )
    args = parser.parse_args()

    search_root = args.path if args.path.is_absolute() else ROOT / args.path

    if not RULES:
        print(
            "No lint rules defined.\n"
            "Add rules to scripts/lint_agent_friendly.py.\n"
            "See docs/quality/linter-guide.md for how to write agent-friendly rules."
        )
        return 0

    violations = run_rules(RULES, search_root)
    errors = [v for v in violations if v[0].severity == "error"]
    warnings = [v for v in violations if v[0].severity == "warning"]

    for rule, filepath, line_num, line in violations:
        rel = filepath.relative_to(ROOT) if filepath.is_relative_to(ROOT) else filepath
        severity_label = rule.severity.upper()
        print(f"{rel}:{line_num}: [{rule.id}] {severity_label} — {rule.description}")
        print(f"  Found: {line.strip()}")
        print(f"  Fix: {rule.remediation}")
        print()

    if violations:
        print(
            f"Found {len(errors)} error(s) and {len(warnings)} warning(s). "
            "Each violation above includes a Fix instruction — apply it and re-run."
        )

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
