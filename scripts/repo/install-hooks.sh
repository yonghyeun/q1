#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "${ROOT_DIR}"

git config core.hooksPath .githooks

HOOK_TARGETS=(
  ".githooks/commit-msg"
  ".githooks/pre-commit"
  ".githooks/pre-push"
)

for target in "${HOOK_TARGETS[@]}"; do
  if [[ -f "${target}" ]]; then
    chmod +x "${target}"
  fi
done

if [[ -d ".githooks/pre-commit.d" ]]; then
  while IFS= read -r -d '' hook; do
    chmod +x "${hook}"
  done < <(find ".githooks/pre-commit.d" -maxdepth 1 -type f -print0)
fi

echo "✅ Git hooks 설치 완료"
echo "   - core.hooksPath=.githooks"
