#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(git rev-parse --show-toplevel)"
cd "${ROOT_DIR}"

usage() {
  cat <<'EOH'
사용법:
  ./skills/public/gh-flow-orchestrator/scripts/run_flow.sh \
    --mode <start|open-pr|merge|full> \
    [--branch config/wbs-governance-reset] \
    [--type feature|bug|chore] \
    [--issue 1234] \
    [--title "이슈 제목"] \
    [--issue-body-file /tmp/issue.md] \
    [--pr-title "[config] PR 제목"] \
    [--pr-body-file /tmp/pr.md] \
    [--merge-method squash|merge|rebase] \
    [--merge-subject "머지 커밋 제목"] \
    [--dry-run]
EOH
}

MODE=""
BRANCH_NAME=""
TYPE=""
ISSUE_NUMBER=""
TITLE=""
ISSUE_BODY_FILE=""
PR_TITLE=""
PR_BODY_FILE=""
MERGE_METHOD="squash"
MERGE_SUBJECT=""
DRY_RUN=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --mode) MODE="${2:-}"; shift 2 ;;
    --branch) BRANCH_NAME="${2:-}"; shift 2 ;;
    --type) TYPE="${2:-}"; shift 2 ;;
    --issue) ISSUE_NUMBER="${2:-}"; shift 2 ;;
    --title) TITLE="${2:-}"; shift 2 ;;
    --issue-body-file) ISSUE_BODY_FILE="${2:-}"; shift 2 ;;
    --pr-title) PR_TITLE="${2:-}"; shift 2 ;;
    --pr-body-file) PR_BODY_FILE="${2:-}"; shift 2 ;;
    --merge-method) MERGE_METHOD="${2:-}"; shift 2 ;;
    --merge-subject) MERGE_SUBJECT="${2:-}"; shift 2 ;;
    --dry-run) DRY_RUN=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "알 수 없는 옵션: $1" >&2; usage; exit 1 ;;
  esac
done

if [[ -z "${MODE}" ]]; then
  usage
  exit 1
fi

run_cmd() {
  if [[ ${DRY_RUN} -eq 1 ]]; then
    echo "[dry-run] $*"
  else
    "$@"
  fi
}

create_issue_if_needed() {
  if [[ -n "${ISSUE_NUMBER}" ]]; then
    return
  fi

  if [[ -z "${TYPE}" || -z "${TITLE}" || -z "${ISSUE_BODY_FILE}" ]]; then
    echo "❌ issue 생성에는 --type, --title, --issue-body-file이 필요합니다." >&2
    exit 1
  fi

  if [[ ${DRY_RUN} -eq 1 ]]; then
    echo "[dry-run] ./scripts/repo/issue_create.sh --type ${TYPE} --title \"${TITLE}\" --body-file ${ISSUE_BODY_FILE}"
    ISSUE_NUMBER="0000"
    return
  fi

  OUTPUT="$(./scripts/repo/issue_create.sh --type "${TYPE}" --title "${TITLE}" --body-file "${ISSUE_BODY_FILE}")"
  echo "${OUTPUT}"
  ISSUE_NUMBER="$(printf '%s\n' "${OUTPUT}" | awk '/number:/ {print $3}' | tail -n1)"
  if [[ -z "${ISSUE_NUMBER}" ]]; then
    echo "❌ issue 번호를 파싱할 수 없습니다." >&2
    exit 1
  fi
}

start_branch() {
  if [[ -z "${BRANCH_NAME}" ]]; then
    echo "❌ start/full 모드는 --branch가 필요합니다." >&2
    exit 1
  fi

  if [[ ${DRY_RUN} -eq 1 ]]; then
    echo "[dry-run] git switch main"
    echo "[dry-run] git pull --ff-only"
    echo "[dry-run] git switch -c ${BRANCH_NAME}"
    echo "[dry-run] python3 scripts/repo/branch_guard.py validate-name --branch ${BRANCH_NAME}"
    return
  fi

  git switch main
  git pull --ff-only
  git switch -c "${BRANCH_NAME}"
  python3 scripts/repo/branch_guard.py validate-name --branch "${BRANCH_NAME}"
}

case "${MODE}" in
  start)
    start_branch
    ;;
  open-pr)
    if [[ -z "${PR_TITLE}" || -z "${PR_BODY_FILE}" ]]; then
      echo "❌ open-pr 모드는 --pr-title, --pr-body-file이 필요합니다." >&2
      exit 1
    fi
    if [[ ${DRY_RUN} -eq 1 ]]; then
      run_cmd ./scripts/repo/pr_create.sh --title "${PR_TITLE}" --body-file "${PR_BODY_FILE}" --dry-run
    else
      run_cmd ./scripts/repo/pr_create.sh --title "${PR_TITLE}" --body-file "${PR_BODY_FILE}"
    fi
    ;;
  merge)
    MERGE_ARGS=(./scripts/repo/pr_merge.sh --method "${MERGE_METHOD}")
    if [[ -n "${MERGE_SUBJECT}" ]]; then
      MERGE_ARGS+=(--subject "${MERGE_SUBJECT}")
    fi
    if [[ ${DRY_RUN} -eq 1 ]]; then
      MERGE_ARGS+=(--dry-run)
    fi
    run_cmd "${MERGE_ARGS[@]}"
    ;;
  full)
    if [[ -z "${BRANCH_NAME}" || -z "${PR_TITLE}" || -z "${PR_BODY_FILE}" ]]; then
      echo "❌ full 모드는 --branch, --pr-title, --pr-body-file가 필요합니다." >&2
      exit 1
    fi
    create_issue_if_needed
    start_branch
    if [[ ${DRY_RUN} -eq 1 ]]; then
      run_cmd ./scripts/repo/pr_create.sh --title "${PR_TITLE}" --body-file "${PR_BODY_FILE}" --dry-run
    else
      run_cmd ./scripts/repo/pr_create.sh --title "${PR_TITLE}" --body-file "${PR_BODY_FILE}"
    fi
    ;;
  *)
    echo "❌ 지원하지 않는 mode: ${MODE}" >&2
    usage
    exit 1
    ;;
esac

echo "✅ flow mode '${MODE}' 완료"
