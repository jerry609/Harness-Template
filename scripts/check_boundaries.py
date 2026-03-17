#!/usr/bin/env python3
"""Check module boundary violations.

This script enforces architectural boundaries by scanning import statements.
Error messages are written as remediation instructions so agents can self-correct.

Usage:
    python scripts/check_boundaries.py
    python scripts/check_boundaries.py --config boundaries.yml

Customize BOUNDARIES below or supply a YAML config file.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# ---------------------------------------------------------------------------
# Define boundaries inline. Replace these with your real project modules.
# Each entry: (source_glob, forbidden_pattern, remediation)
# ---------------------------------------------------------------------------
BOUNDARIES: list[tuple[str, str, str]] = [
    # Example: domain layer must not import from infrastructure
    # (
    #     "src/domain/**/*.py",
    #     r"from src\.infra|import src\.infra",
    #     "Domain must not import infrastructure. "
    #     "Move the dependency behind a domain interface and inject it from the composition root."
    # ),
    # Example: API layer must not import CLI internals
    # (
    #     "src/api/**/*.py",
    #     r"from src\.cli|import src\.cli",
    #     "API layer must not depend on CLI. "
    #     "Extract the shared logic into src/shared/ and import from there."
    # ),
]


def load_yaml_config(config_path: Path) -> list[tuple[str, str, str]]:
    """Load boundaries from a YAML config file."""
    try:
        import yaml  # type: ignore[import-untyped]
    except ImportError:
        print(
            "PyYAML is required to load boundaries.yml. "
            "Install it with: pip install pyyaml\n"
            "Alternatively, define boundaries inline in this script."
        )
        sys.exit(1)

    data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    rules: list[tuple[str, str, str]] = []
    for entry in data.get("boundaries", []):
        module = entry["module"].rstrip("/")
        forbidden = entry.get("forbidden", [])
        reason = entry.get("reason", "Boundary violation.")
        for dep in forbidden:
            dep_escaped = re.escape(dep.rstrip("/")).replace("/", r"[./]")
            pattern = rf"from\s+{dep_escaped}|import\s+{dep_escaped}"
            glob_pattern = f"{module}/**/*.py"
            rules.append((glob_pattern, pattern, reason))
    return rules


def check(boundaries: list[tuple[str, str, str]]) -> list[str]:
    errors: list[str] = []
    for source_glob, forbidden_re, remediation in boundaries:
        compiled = re.compile(forbidden_re)
        for filepath in ROOT.glob(source_glob):
            if not filepath.is_file():
                continue
            try:
                content = filepath.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            for line_num, line in enumerate(content.splitlines(), start=1):
                if compiled.search(line):
                    rel = filepath.relative_to(ROOT)
                    errors.append(
                        f"{rel}:{line_num}: BOUNDARY VIOLATION\n"
                        f"  Found: {line.strip()}\n"
                        f"  Fix: {remediation}"
                    )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Check module boundary violations.")
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Path to boundaries.yml config file.",
    )
    args = parser.parse_args()

    boundaries = list(BOUNDARIES)
    if args.config:
        config_path = ROOT / args.config if not args.config.is_absolute() else args.config
        if config_path.exists():
            boundaries.extend(load_yaml_config(config_path))
        else:
            print(f"Config file not found: {config_path}")
            return 1
    else:
        default_config = ROOT / "boundaries.yml"
        if default_config.exists():
            boundaries.extend(load_yaml_config(default_config))

    if not boundaries:
        print(
            "No boundary rules defined.\n"
            "Add rules to scripts/check_boundaries.py or create boundaries.yml.\n"
            "See docs/architecture/boundaries.md for guidance."
        )
        return 0

    errors = check(boundaries)
    if errors:
        print("Boundary violations found:\n")
        for error in errors:
            print(error)
            print()
        print(
            f"{len(errors)} violation(s) found. "
            "Each error above includes a Fix instruction — apply it and re-run."
        )
        return 1

    print("All boundary checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
