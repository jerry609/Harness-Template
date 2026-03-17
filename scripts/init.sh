#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 1 ]; then
  echo "Usage: ./scripts/init.sh <slug> [title]"
  exit 1
fi

python scripts/init_task.py "$@"