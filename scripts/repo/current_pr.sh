#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "${ROOT_DIR}"

usage() {
  cat <<'EOF'
사용법:
  ./scripts/repo/current_pr.sh
  ./scripts/repo/current_pr.sh --live
EOF
}

LIVE_MODE=0
while [[ $# -gt 0 ]]; do
  case "${1:-}" in
    --live)
      LIVE_MODE=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "❌ 알 수 없는 옵션: $1" >&2
      usage
      exit 1
      ;;
  esac
done

extract_live_field() {
  local json_input="$1"
  local field_name="$2"
  python3 -c '
import json
import sys

data = json.loads(sys.argv[1])
field = sys.argv[2]
value = data.get(field, "")
if value is None:
    value = ""
print(value)
' "${json_input}" "${field_name}"
}

METADATA_OUTPUT="$(./scripts/repo/worktree_pr_metadata.sh read)"

if [[ -z "${METADATA_OUTPUT}" ]]; then
  echo "현재 worktree에 연결된 PR 없음"
  exit 0
fi

get_value() {
  local key="$1"
  printf '%s\n' "${METADATA_OUTPUT}" | sed -n "s/^${key}=//p" | head -n 1
}

PR_NUMBER="$(get_value "q1.pr.number")"
PR_URL="$(get_value "q1.pr.url")"
PR_TITLE="$(get_value "q1.pr.title")"
PR_STATE_AT_RECORD="$(get_value "q1.pr.state")"
PR_BASE_BRANCH="$(get_value "q1.pr.baseBranch")"
PR_HEAD_BRANCH="$(get_value "q1.pr.headBranch")"
PR_WORKTREE="$(get_value "q1.pr.worktree")"
PR_RECORDED_AT="$(get_value "q1.pr.recordedAt")"
PR_RECORDED_BY="$(get_value "q1.pr.recordedBy")"

LIVE_PR_TITLE=""
LIVE_PR_URL=""
LIVE_PR_STATE=""
LIVE_PR_IS_DRAFT=""
LIVE_PR_BASE_BRANCH=""
LIVE_PR_HEAD_BRANCH=""
LIVE_WARNING=""

if [[ ${LIVE_MODE} -eq 1 && -n "${PR_NUMBER}" ]]; then
  if ./scripts/repo/gh_preflight.sh --require-api >/dev/null 2>&1; then
    if LIVE_OUTPUT="$(gh pr view "${PR_NUMBER}" --json number,title,url,state,isDraft,baseRefName,headRefName 2>&1)"; then
      LIVE_PR_TITLE="$(extract_live_field "${LIVE_OUTPUT}" "title")"
      LIVE_PR_URL="$(extract_live_field "${LIVE_OUTPUT}" "url")"
      LIVE_PR_STATE="$(extract_live_field "${LIVE_OUTPUT}" "state")"
      LIVE_PR_IS_DRAFT="$(extract_live_field "${LIVE_OUTPUT}" "isDraft")"
      LIVE_PR_BASE_BRANCH="$(extract_live_field "${LIVE_OUTPUT}" "baseRefName")"
      LIVE_PR_HEAD_BRANCH="$(extract_live_field "${LIVE_OUTPUT}" "headRefName")"
    else
      LIVE_WARNING="live 조회 실패. recorded snapshot만 표시"
    fi
  else
    LIVE_WARNING="gh preflight 실패. recorded snapshot만 표시"
  fi
fi

echo "현재 worktree 연결 PR"
if [[ -n "${PR_NUMBER}" ]]; then
  echo "- 번호: #${PR_NUMBER}"
fi
if [[ -n "${PR_TITLE}" ]]; then
  echo "- 제목: ${PR_TITLE}"
fi
if [[ -n "${PR_URL}" ]]; then
  echo "- URL: ${PR_URL}"
fi
if [[ -n "${PR_STATE_AT_RECORD}" ]]; then
  echo "- 기록 state: ${PR_STATE_AT_RECORD}"
fi
if [[ -n "${PR_BASE_BRANCH}" ]]; then
  echo "- base 브랜치: ${PR_BASE_BRANCH}"
fi
if [[ -n "${PR_HEAD_BRANCH}" ]]; then
  echo "- head 브랜치: ${PR_HEAD_BRANCH}"
fi
if [[ -n "${PR_WORKTREE}" ]]; then
  echo "- 워크트리: ${PR_WORKTREE}"
fi
if [[ -n "${PR_RECORDED_AT}" ]]; then
  echo "- 기록 시각: ${PR_RECORDED_AT}"
fi
if [[ -n "${PR_RECORDED_BY}" ]]; then
  echo "- 기록 주체: ${PR_RECORDED_BY}"
fi

if [[ ${LIVE_MODE} -eq 1 && -n "${PR_NUMBER}" ]]; then
  echo
  echo "GitHub live 상태"
  if [[ -n "${LIVE_WARNING}" ]]; then
    echo "- 상태: ${LIVE_WARNING}"
  fi
  if [[ -n "${LIVE_PR_TITLE}" ]]; then
    echo "- 제목: ${LIVE_PR_TITLE}"
  fi
  if [[ -n "${LIVE_PR_URL}" ]]; then
    echo "- URL: ${LIVE_PR_URL}"
  fi
  if [[ -n "${LIVE_PR_STATE}" ]]; then
    echo "- 현재 state: ${LIVE_PR_STATE}"
  fi
  if [[ -n "${LIVE_PR_IS_DRAFT}" ]]; then
    echo "- 현재 draft: ${LIVE_PR_IS_DRAFT}"
  fi
  if [[ -n "${LIVE_PR_BASE_BRANCH}" ]]; then
    echo "- 현재 base 브랜치: ${LIVE_PR_BASE_BRANCH}"
  fi
  if [[ -n "${LIVE_PR_HEAD_BRANCH}" ]]; then
    echo "- 현재 head 브랜치: ${LIVE_PR_HEAD_BRANCH}"
  fi
fi
