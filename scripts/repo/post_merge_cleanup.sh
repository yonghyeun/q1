#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "${ROOT_DIR}"

MERGED_BRANCH="${1:-}"

if [[ -z "${MERGED_BRANCH}" ]]; then
  echo "사용법: $0 <merged-branch-name>" >&2
  exit 1
fi

if ! git remote get-url origin >/dev/null 2>&1; then
  echo "❌ origin remote가 없습니다." >&2
  echo "   예시: git remote add origin <github-repo-url>" >&2
  exit 1
fi

CURRENT_BRANCH="$(git branch --show-current)"
if [[ "${CURRENT_BRANCH}" == "${MERGED_BRANCH}" ]]; then
  git switch main
fi

git fetch origin --prune
git pull --ff-only origin main
git branch -d "${MERGED_BRANCH}"

echo "✅ merge 후 로컬 정리 완료: ${MERGED_BRANCH}"
