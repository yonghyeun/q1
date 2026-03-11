#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "${ROOT_DIR}"

usage() {
  cat <<'EOF'
사용법:
  ./scripts/repo/current_issue.sh
  ./scripts/repo/current_issue.sh --live
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

extract_live_status() {
  local json_input="$1"
  python3 -c '
import json
import sys

data = json.loads(sys.argv[1])
for label in data.get("labels", []):
    name = label.get("name", "")
    if name.startswith("status:"):
        print(name)
        break
' "${json_input}"
}

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

LIVE_ISSUE_TITLE=""
LIVE_ISSUE_URL=""
LIVE_ISSUE_STATE=""
LIVE_ISSUE_STATUS=""

if [[ ${LIVE_MODE} -eq 1 && -n "${ISSUE_NUMBER}" ]]; then
  ./scripts/repo/gh_preflight.sh >/dev/null || {
    echo "❌ live issue 조회 전 gh preflight에 실패했습니다." >&2
    echo "다음 행동: gh 인증과 origin remote 상태를 확인한 뒤 다시 실행하세요." >&2
    exit 10
  }

  LIVE_OUTPUT="$(gh issue view "${ISSUE_NUMBER}" --json number,title,url,state,labels 2>&1)" || {
    echo "❌ issue #${ISSUE_NUMBER} live 조회에 실패했습니다." >&2
    echo "다음 행동: 네트워크와 gh 인증 상태를 확인한 뒤 다시 실행하세요." >&2
    exit 11
  }

  LIVE_ISSUE_TITLE="$(extract_live_field "${LIVE_OUTPUT}" "title")"
  LIVE_ISSUE_URL="$(extract_live_field "${LIVE_OUTPUT}" "url")"
  LIVE_ISSUE_STATE="$(extract_live_field "${LIVE_OUTPUT}" "state")"
  LIVE_ISSUE_STATUS="$(extract_live_status "${LIVE_OUTPUT}")"
fi

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

if [[ ${LIVE_MODE} -eq 1 && -n "${ISSUE_NUMBER}" ]]; then
  echo
  echo "GitHub live 상태"
  if [[ -n "${LIVE_ISSUE_TITLE}" ]]; then
    echo "- 제목: ${LIVE_ISSUE_TITLE}"
  fi
  if [[ -n "${LIVE_ISSUE_URL}" ]]; then
    echo "- URL: ${LIVE_ISSUE_URL}"
  fi
  if [[ -n "${LIVE_ISSUE_STATE}" ]]; then
    echo "- 현재 state: ${LIVE_ISSUE_STATE}"
  fi
  if [[ -n "${LIVE_ISSUE_STATUS}" ]]; then
    echo "- 현재 status label: ${LIVE_ISSUE_STATUS}"
  fi
fi
