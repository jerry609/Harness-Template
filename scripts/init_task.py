#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC_TEMPLATE = ROOT / "docs" / "product-specs" / "TEMPLATE.md"
PLAN_TEMPLATE = ROOT / "docs" / "exec-plans" / "TEMPLATE.md"
FEATURE_LIST = ROOT / "artifacts" / "feature-list.json"


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = value.strip("-")
    return value or "new-task"


def render(template: str, slug: str, title: str, today: str) -> str:
    return (
        template.replace("{{SLUG}}", slug)
        .replace("{{TITLE}}", title)
        .replace("{{DATE}}", today)
    )


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python scripts/init_task.py <slug> [title]")
        return 1

    raw_slug = sys.argv[1]
    slug = slugify(raw_slug)
    title = sys.argv[2] if len(sys.argv) > 2 else slug.replace("-", " ").title()
    today = str(date.today())

    spec_path = ROOT / "docs" / "product-specs" / f"{slug}.md"
    plan_path = ROOT / "docs" / "exec-plans" / f"{slug}.md"

    if spec_path.exists() or plan_path.exists():
        print(f"Refusing to overwrite existing task files for '{slug}'.")
        return 1

    spec_text = render(SPEC_TEMPLATE.read_text(encoding="utf-8"), slug, title, today)
    plan_text = render(PLAN_TEMPLATE.read_text(encoding="utf-8"), slug, title, today)

    spec_path.write_text(spec_text, encoding="utf-8", newline="\n")
    plan_path.write_text(plan_text, encoding="utf-8", newline="\n")

    data = json.loads(FEATURE_LIST.read_text(encoding="utf-8"))
    features = data.setdefault("features", [])
    if any(item.get("id") == slug for item in features):
        print(f"Feature id '{slug}' already exists in artifacts/feature-list.json.")
        return 1

    features.append(
        {
            "id": slug,
            "title": title,
            "status": "backlog",
            "spec": f"docs/product-specs/{slug}.md",
            "plan": f"docs/exec-plans/{slug}.md",
            "owner": "unassigned",
        }
    )
    data["updated_at"] = today
    FEATURE_LIST.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n")

    print(f"Created {spec_path.relative_to(ROOT)}")
    print(f"Created {plan_path.relative_to(ROOT)}")
    print("Updated artifacts/feature-list.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())