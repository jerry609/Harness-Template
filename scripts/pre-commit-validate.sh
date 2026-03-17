#!/usr/bin/env bash
# Pre-commit harness validation.
# Runs lightweight checks before every commit to catch harness drift early.
#
# This script is called by .pre-commit-config.yaml and can also be run manually:
#   bash scripts/pre-commit-validate.sh

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ERRORS=0

# ---- Check that required files exist ----
required_files=(
    "AGENTS.md"
    "artifacts/progress.md"
    "artifacts/feature-list.json"
    "artifacts/decisions.md"
)

for f in "${required_files[@]}"; do
    if [ ! -f "$ROOT/$f" ]; then
        echo "ERROR: Missing required file: $f"
        echo "  Fix: Create the file or restore it from the template."
        ERRORS=$((ERRORS + 1))
    fi
done

# ---- Check that feature-list.json is valid JSON ----
if [ -f "$ROOT/artifacts/feature-list.json" ]; then
    if ! python3 -c "import json; json.load(open('$ROOT/artifacts/feature-list.json'))" 2>/dev/null; then
        echo "ERROR: artifacts/feature-list.json is not valid JSON."
        echo "  Fix: Check for syntax errors (missing commas, trailing commas, unquoted keys)."
        ERRORS=$((ERRORS + 1))
    fi
fi

# ---- Check that progress.md has required sections ----
if [ -f "$ROOT/artifacts/progress.md" ]; then
    required_headings=("# Progress" "## Current focus" "## Next action" "## Blockers")
    for heading in "${required_headings[@]}"; do
        if ! grep -q "$heading" "$ROOT/artifacts/progress.md"; then
            echo "ERROR: artifacts/progress.md is missing heading: $heading"
            echo "  Fix: Add the '$heading' section to progress.md."
            ERRORS=$((ERRORS + 1))
        fi
    done
fi

# ---- Summary ----
if [ "$ERRORS" -gt 0 ]; then
    echo ""
    echo "$ERRORS pre-commit error(s) found. Fix the issues above and try again."
    exit 1
fi

echo "Pre-commit harness checks passed."
exit 0
