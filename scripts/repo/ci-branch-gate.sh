#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "${ROOT_DIR}"

resolve_branch() {
  if [[ -n "${GITHUB_HEAD_REF:-}" ]]; then
    printf '%s' "${GITHUB_HEAD_REF}"
    return
  fi
  if [[ -n "${GITHUB_REF_NAME:-}" ]]; then
    printf '%s' "${GITHUB_REF_NAME}"
    return
  fi
  if [[ -n "${CI_COMMIT_REF_NAME:-}" ]]; then
    printf '%s' "${CI_COMMIT_REF_NAME}"
    return
  fi
  git branch --show-current
}

BRANCH="${1:-$(resolve_branch)}"

if [[ -z "${BRANCH}" ]]; then
  echo "❌ CI branch gate: 브랜치명을 확인할 수 없습니다." >&2
  exit 1
fi

if [[ "${BRANCH}" == "main" ]]; then
  echo "ℹ️ main 브랜치에서는 branch gate를 건너뜁니다 (PR head branch 전용 검사)."
  exit 0
fi

python3 scripts/repo/branch_guard.py validate-name --branch "${BRANCH}"
python3 scripts/repo/branch_guard.py validate-context --branch "${BRANCH}"
python3 scripts/repo/branch_guard.py validate-pr --branch "${BRANCH}"
