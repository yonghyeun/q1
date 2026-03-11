#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "${ROOT_DIR}"

usage() {
  cat <<'EOF'
사용법:
  ./scripts/repo/current_issue.sh
EOF
}

if [[ $# -gt 0 ]]; then
  case "${1:-}" in
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
fi

METADATA_OUTPUT="$(./scripts/repo/worktree_issue_metadata.sh read)"

if [[ -z "${METADATA_OUTPUT}" ]]; then
  echo "현재 worktree에 연결된 issue 없음"
  exit 0
fi

get_value() {
  local key="$1"
  printf '%s\n' "${METADATA_OUTPUT}" | sed -n "s/^${key}=//p" | head -n 1
}

ISSUE_NUMBER="$(get_value "q1.issue.number")"
ISSUE_URL="$(get_value "q1.issue.url")"
ISSUE_TITLE="$(get_value "q1.issue.title")"
ISSUE_STATUS_AT_RECORD="$(get_value "q1.issue.statusAtRecord")"
ISSUE_BRANCH="$(get_value "q1.issue.branch")"
ISSUE_WORKTREE="$(get_value "q1.issue.worktree")"
ISSUE_RECORDED_AT="$(get_value "q1.issue.recordedAt")"
ISSUE_RECORDED_BY="$(get_value "q1.issue.recordedBy")"

echo "현재 worktree 연결 issue"
if [[ -n "${ISSUE_NUMBER}" ]]; then
  echo "- 번호: #${ISSUE_NUMBER}"
fi
if [[ -n "${ISSUE_TITLE}" ]]; then
  echo "- 제목: ${ISSUE_TITLE}"
fi
if [[ -n "${ISSUE_URL}" ]]; then
  echo "- URL: ${ISSUE_URL}"
fi
if [[ -n "${ISSUE_STATUS_AT_RECORD}" ]]; then
  echo "- 기록 상태: ${ISSUE_STATUS_AT_RECORD}"
fi
if [[ -n "${ISSUE_BRANCH}" ]]; then
  echo "- 브랜치: ${ISSUE_BRANCH}"
fi
if [[ -n "${ISSUE_WORKTREE}" ]]; then
  echo "- 워크트리: ${ISSUE_WORKTREE}"
fi
if [[ -n "${ISSUE_RECORDED_AT}" ]]; then
  echo "- 기록 시각: ${ISSUE_RECORDED_AT}"
fi
if [[ -n "${ISSUE_RECORDED_BY}" ]]; then
  echo "- 기록 주체: ${ISSUE_RECORDED_BY}"
fi
