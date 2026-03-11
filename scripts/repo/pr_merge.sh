#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "${ROOT_DIR}"

usage() {
  cat <<'EOF'
사용법:
  ./scripts/repo/pr_merge.sh [--pr <number-or-url>] [--method <squash|merge|rebase>] [--subject "<merge-subject>"] [--dry-run]

예시:
  ./scripts/repo/pr_merge.sh --method squash
  ./scripts/repo/pr_merge.sh --method squash --subject "[config] 브랜치 거버넌스 v1"
  ./scripts/repo/pr_merge.sh --pr 42 --method rebase
EOF
}

fail() {
  local message="$1"
  local next_action="$2"
  echo "❌ ${message}" >&2
  echo "정책: PR merge leaf는 merge 실행만 담당합니다." >&2
  echo "다음 행동: ${next_action}" >&2
  exit 1
}

PR_TARGET=""
METHOD="squash"
SUBJECT=""
DRY_RUN=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --pr)
      PR_TARGET="${2:-}"
      shift 2
      ;;
    --method)
      METHOD="${2:-}"
      shift 2
      ;;
    --subject)
      SUBJECT="${2:-}"
      shift 2
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "알 수 없는 옵션: $1" >&2
      usage
      exit 1
      ;;
  esac
done

case "${METHOD}" in
  squash|merge|rebase) ;;
  *)
    fail "--method 는 squash|merge|rebase 중 하나여야 합니다." "--method 값을 확인한 뒤 다시 실행하세요."
    ;;
esac

python3 scripts/repo/detached_head_guard.py validate-write

BRANCH="$(git branch --show-current)"
if [[ -z "${BRANCH}" ]]; then
  fail "현재 브랜치를 확인할 수 없습니다." "브랜치가 checkout된 worktree에서 다시 실행하거나 --pr 를 명시하세요."
fi

python3 scripts/repo/protected_branch_write_guard.py validate-write --branch "${BRANCH}"
python3 scripts/repo/branch_guard.py validate-name --branch "${BRANCH}"
python3 scripts/repo/dirty_worktree_guard.py validate-clean

if [[ ${DRY_RUN} -eq 0 ]]; then
  ./scripts/repo/gh_preflight.sh --require-api
fi

if [[ -n "${PR_TARGET}" ]]; then
  VIEW_TARGET="${PR_TARGET}"
else
  VIEW_TARGET="${BRANCH}"
fi

if [[ ${DRY_RUN} -eq 0 ]]; then
  gh pr view "${VIEW_TARGET}" --json number,state,mergeStateStatus,isDraft >/dev/null
fi

MERGE_ARGS=(pr merge)
if [[ -n "${PR_TARGET}" ]]; then
  MERGE_ARGS+=("${PR_TARGET}")
fi

case "${METHOD}" in
  squash) MERGE_ARGS+=(--squash) ;;
  merge) MERGE_ARGS+=(--merge) ;;
  rebase) MERGE_ARGS+=(--rebase) ;;
esac

MERGE_SUBJECT=""
if [[ "${METHOD}" == "squash" || "${METHOD}" == "merge" ]]; then
  if [[ -n "${SUBJECT}" ]]; then
    MERGE_SUBJECT="${SUBJECT}"
  else
    if [[ ${DRY_RUN} -eq 0 ]]; then
      MERGE_SUBJECT="$(gh pr view "${VIEW_TARGET}" --json title --jq .title)"
      if [[ -z "${MERGE_SUBJECT}" ]]; then
        fail "PR 제목을 조회할 수 없어 merge subject를 자동 설정할 수 없습니다." "--subject 를 명시하거나 PR 제목을 확인한 뒤 다시 실행하세요."
      fi
    else
      MERGE_SUBJECT="<PR_TITLE_FROM_GH>"
    fi
  fi
elif [[ -n "${SUBJECT}" ]]; then
  echo "⚠️ --method rebase에서는 --subject가 적용되지 않아 무시합니다." >&2
fi

if [[ -n "${MERGE_SUBJECT}" ]]; then
  MERGE_ARGS+=(--subject "${MERGE_SUBJECT}")
fi

if [[ ${DRY_RUN} -eq 1 ]]; then
  PRINT_CMD="gh"
  for arg in "${MERGE_ARGS[@]}"; do
    PRINT_CMD+=" $(printf '%q' "${arg}")"
  done
  echo "✅ dry-run: PR merge 명령"
  echo "${PRINT_CMD}"
  echo "다음 행동: merge 이후 후속 정리가 필요하면 task_end.sh 또는 cleanup leaf를 별도로 실행하세요."
  exit 0
fi

gh "${MERGE_ARGS[@]}"

echo "✅ PR merge 완료: ${BRANCH}"
echo "다음 행동: 후속 정리가 필요하면 task_end.sh 또는 post-merge cleanup shell을 실행하세요."
