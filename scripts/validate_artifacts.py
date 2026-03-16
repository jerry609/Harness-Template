#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = [
    ROOT / "README.md",
    ROOT / "AGENTS.md",
    ROOT / "docs" / "architecture" / "index.md",
    ROOT / "docs" / "quality" / "golden-principles.md",
    ROOT / "docs" / "quality" / "cleanup-checklist.md",
    ROOT / "artifacts" / "progress.md",
    ROOT / "artifacts" / "feature-list.json",
    ROOT / "artifacts" / "decisions.md",
    ROOT / "evals" / "README.md",
]
VALID_STATUSES = {"backlog", "in_progress", "blocked", "done"}
REQUIRED_PROGRESS_HEADINGS = [
    "# Progress",
    "## Current focus",
    "## Last verified state",
    "## Next action",
    "## Blockers",
    "## Session log",
]


def main() -> int:
    errors: list[str] = []

    for path in REQUIRED_FILES:
        if not path.exists():
            errors.append(f"Missing required file: {path.relative_to(ROOT)}")

    progress_path = ROOT / "artifacts" / "progress.md"
    if progress_path.exists():
        progress_text = progress_path.read_text(encoding="utf-8")
        for heading in REQUIRED_PROGRESS_HEADINGS:
            if heading not in progress_text:
                errors.append(f"Progress file is missing heading: {heading}")

    feature_path = ROOT / "artifacts" / "feature-list.json"
    if feature_path.exists():
        try:
            data = json.loads(feature_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"feature-list.json is invalid JSON: {exc}")
        else:
            features = data.get("features")
            if not isinstance(features, list) or not features:
                errors.append("feature-list.json must contain a non-empty 'features' list")
            else:
                for index, item in enumerate(features):
                    prefix = f"feature-list.json entry {index}"
                    if not isinstance(item, dict):
                        errors.append(f"{prefix} must be an object")
                        continue
                    for key in ("id", "title", "status", "spec", "plan", "owner"):
                        if not item.get(key):
                            errors.append(f"{prefix} is missing '{key}'")
                    status = item.get("status")
                    if status and status not in VALID_STATUSES:
                        errors.append(
                            f"{prefix} has invalid status '{status}'. Valid: {sorted(VALID_STATUSES)}"
                        )
                    for key in ("spec", "plan"):
                        rel = item.get(key)
                        if rel:
                            path = ROOT / rel
                            if not path.exists():
                                errors.append(f"{prefix} points to missing file: {rel}")

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())