#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "${ROOT_DIR}"
echo "ℹ️ pr_finalize.sh 는 deprecated 경로입니다. task_end.sh 로 위임합니다."
exec ./scripts/repo/task_end.sh "$@"
