#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "${ROOT_DIR}"

if [[ $# -eq 1 && "${1:-}" != -* ]]; then
  exec ./scripts/repo/post_merge_branch_cleanup.sh --branch "$1"
fi

exec ./scripts/repo/post_merge_branch_cleanup.sh "$@"
