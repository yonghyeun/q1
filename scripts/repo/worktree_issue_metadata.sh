#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "${ROOT_DIR}"

EXIT_INVALID_INPUT=1

KEYS=(
  q1.issue.number
  q1.issue.url
  q1.issue.title
  q1.issue.statusAtRecord
  q1.issue.branch
  q1.issue.worktree
  q1.issue.recordedAt
  q1.issue.recordedBy
)

usage() {
  cat <<'EOF'
사용법:
  ./scripts/repo/worktree_issue_metadata.sh write --number <n> --url <url> --branch <branch> --worktree <path> --recorded-at <iso8601> [--title <title>] [--status-at-record <status>] [--recorded-by <actor>]
  ./scripts/repo/worktree_issue_metadata.sh read
  ./scripts/repo/worktree_issue_metadata.sh clear
EOF
}

set_or_unset() {
  local key="$1"
  local value="$2"

  if [[ -n "${value}" ]]; then
    git config --worktree "${key}" "${value}"
    return
  fi

  git config --worktree --unset-all "${key}" >/dev/null 2>&1 || true
}

emit_key_if_present() {
  local key="$1"
  local value=""
  value="$(git config --worktree --get "${key}" 2>/dev/null || true)"
  if [[ -n "${value}" ]]; then
    echo "${key}=${value}"
  fi
}

MODE="${1:-}"
if [[ -z "${MODE}" ]]; then
  usage
  exit "${EXIT_INVALID_INPUT}"
fi
shift || true

case "${MODE}" in
  write)
    NUMBER=""
    URL=""
    TITLE=""
    STATUS_AT_RECORD=""
    BRANCH=""
    WORKTREE=""
    RECORDED_AT=""
    RECORDED_BY="task_start"

    while [[ $# -gt 0 ]]; do
      case "$1" in
        --number)
          NUMBER="${2:-}"
          shift 2
          ;;
        --url)
          URL="${2:-}"
          shift 2
          ;;
        --title)
          TITLE="${2:-}"
          shift 2
          ;;
        --status-at-record)
          STATUS_AT_RECORD="${2:-}"
          shift 2
          ;;
        --branch)
          BRANCH="${2:-}"
          shift 2
          ;;
        --worktree)
          WORKTREE="${2:-}"
          shift 2
          ;;
        --recorded-at)
          RECORDED_AT="${2:-}"
          shift 2
          ;;
        --recorded-by)
          RECORDED_BY="${2:-}"
          shift 2
          ;;
        -h|--help)
          usage
          exit 0
          ;;
        *)
          echo "❌ 알 수 없는 옵션: $1" >&2
          usage
          exit "${EXIT_INVALID_INPUT}"
          ;;
      esac
    done

    if [[ -z "${NUMBER}" || -z "${URL}" || -z "${BRANCH}" || -z "${WORKTREE}" || -z "${RECORDED_AT}" ]]; then
      echo "❌ write에는 --number, --url, --branch, --worktree, --recorded-at 이 필요합니다." >&2
      echo "다음 행동: 필수 issue metadata를 모두 채운 뒤 다시 실행하세요." >&2
      exit "${EXIT_INVALID_INPUT}"
    fi

    ./scripts/repo/worktree_config_bootstrap.sh ensure >/dev/null

    set_or_unset q1.issue.number "${NUMBER}"
    set_or_unset q1.issue.url "${URL}"
    set_or_unset q1.issue.title "${TITLE}"
    set_or_unset q1.issue.statusAtRecord "${STATUS_AT_RECORD}"
    set_or_unset q1.issue.branch "${BRANCH}"
    set_or_unset q1.issue.worktree "${WORKTREE}"
    set_or_unset q1.issue.recordedAt "${RECORDED_AT}"
    set_or_unset q1.issue.recordedBy "${RECORDED_BY}"

    echo "✅ worktree issue metadata 기록 완료: #${NUMBER}"
    ;;

  read)
    if [[ "$(git config --get --bool extensions.worktreeConfig || true)" != "true" ]]; then
      exit 0
    fi

    for key in "${KEYS[@]}"; do
      emit_key_if_present "${key}"
    done
    ;;

  clear)
    if [[ "$(git config --get --bool extensions.worktreeConfig || true)" != "true" ]]; then
      echo "✅ worktree issue metadata 정리 완료: no-op"
      exit 0
    fi

    for key in "${KEYS[@]}"; do
      git config --worktree --unset-all "${key}" >/dev/null 2>&1 || true
    done
    echo "✅ worktree issue metadata 정리 완료"
    ;;

  -h|--help)
    usage
    ;;

  *)
    echo "❌ 지원하지 않는 모드입니다: ${MODE}" >&2
    usage
    exit "${EXIT_INVALID_INPUT}"
    ;;
esac
