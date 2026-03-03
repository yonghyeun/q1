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
    echo "❌ --method 는 squash|merge|rebase 중 하나여야 합니다." >&2
    exit 1
    ;;
esac

if [[ ${DRY_RUN} -eq 0 ]]; then
  ./scripts/repo/gh_preflight.sh
fi

BRANCH="$(git branch --show-current)"
if [[ -z "${BRANCH}" ]]; then
  echo "❌ 현재 브랜치를 확인할 수 없습니다." >&2
  exit 1
fi

if [[ "${BRANCH}" == "main" ]]; then
  echo "❌ main 브랜치에서는 pr_merge를 실행할 수 없습니다." >&2
  exit 1
fi

python3 scripts/repo/branch_guard.py validate-name --branch "${BRANCH}"

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
        echo "❌ PR 제목을 조회할 수 없어 merge subject를 자동 설정할 수 없습니다." >&2
        exit 1
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

MERGE_ARGS+=(--delete-branch)

if [[ ${DRY_RUN} -eq 1 ]]; then
  PRINT_CMD="gh"
  for arg in "${MERGE_ARGS[@]}"; do
    PRINT_CMD+=" $(printf '%q' "${arg}")"
  done
  echo "✅ dry-run: PR merge 명령"
  echo "${PRINT_CMD}"
  echo "./scripts/repo/post_merge_cleanup.sh ${BRANCH}"
  exit 0
fi

gh "${MERGE_ARGS[@]}"
./scripts/repo/post_merge_cleanup.sh "${BRANCH}"

echo "✅ PR merge 및 브랜치 정리 완료: ${BRANCH}"
