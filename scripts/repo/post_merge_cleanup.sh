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
if ! git pull --rebase origin main; then
  echo "❌ main 브랜치 rebase pull에 실패했습니다." >&2
  echo "   충돌이 발생했다면 아래 순서로 수동 정리 후 다시 실행하세요." >&2
  echo "   1) git status" >&2
  echo "   2) (필요 시) git rebase --abort" >&2
  echo "   3) 충돌 해결 후 git pull --rebase origin main" >&2
  exit 1
fi

if git show-ref --verify --quiet "refs/heads/${MERGED_BRANCH}"; then
  git branch -d "${MERGED_BRANCH}"
else
  echo "ℹ️ 로컬 브랜치가 이미 없습니다: ${MERGED_BRANCH}"
fi

echo "✅ merge 후 로컬 정리 완료: ${MERGED_BRANCH}"
