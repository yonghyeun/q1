#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "${ROOT_DIR}"

usage() {
  cat <<'EOF'
사용법:
  ./scripts/repo/task_start.sh --branch <type/slug> [--issue <number>] [--purpose <purpose>] [--base <ref>] [--path-root <dir>] [--apply --yes]

예시:
  ./scripts/repo/task_start.sh --branch feature/signup-flow
  ./scripts/repo/task_start.sh --branch chore/task-start-issue-transition --issue 15
  ./scripts/repo/task_start.sh --branch fix/token-refresh-race --purpose fix
  ./scripts/repo/task_start.sh --branch feature/signup-flow --issue 42 --apply --yes
EOF
}

fail() {
  local message="$1"
  local next_action="$2"
  echo "❌ ${message}" >&2
  echo "정책: task start core는 dry-run이 기본이며, 실제 실행은 --apply --yes로만 수행합니다." >&2
  echo "다음 행동: ${next_action}" >&2
  exit 1
}

realpath_py() {
  python3 -c 'import os,sys; print(os.path.realpath(sys.argv[1]))' "$1"
}

extract_issue_field() {
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

extract_issue_status_labels() {
  local json_input="$1"
  python3 -c '
import json
import sys

data = json.loads(sys.argv[1])
for label in data.get("labels", []):
    name = label.get("name", "")
    if name.startswith("status:"):
        print(name)
' "${json_input}"
}

BRANCH=""
ISSUE_NUMBER=""
PURPOSE="impl"
BASE="main"
PATH_ROOT=".."
APPLY=0
ASSUME_YES=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --branch)
      BRANCH="${2:-}"
      shift 2
      ;;
    --issue)
      ISSUE_NUMBER="${2:-}"
      shift 2
      ;;
    --purpose)
      PURPOSE="${2:-}"
      shift 2
      ;;
    --base)
      BASE="${2:-}"
      shift 2
      ;;
    --path-root)
      PATH_ROOT="${2:-}"
      shift 2
      ;;
    --apply)
      APPLY=1
      shift
      ;;
    --yes)
      ASSUME_YES=1
      shift
      ;;
    --dry-run)
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      fail "알 수 없는 옵션: $1" "사용법을 확인한 뒤 다시 실행하세요."
      ;;
  esac
done

if [[ -z "${BRANCH}" ]]; then
  usage
  fail "--branch 는 필수입니다." "--branch <type/slug> 를 지정해서 다시 실행하세요."
fi

if [[ -n "${ISSUE_NUMBER}" && ! "${ISSUE_NUMBER}" =~ ^[0-9]+$ ]]; then
  fail "--issue 는 숫자 issue 번호여야 합니다." "--issue <number> 형식으로 다시 실행하세요."
fi

case "${PURPOSE}" in
  impl|review|fix|verify|docs|ops) ;;
  *)
    fail "--purpose 는 impl|review|fix|verify|docs|ops 중 하나여야 합니다." "--purpose 값을 허용된 값 중 하나로 수정해서 다시 실행하세요."
    ;;
esac

if [[ ${ASSUME_YES} -eq 1 && ${APPLY} -eq 0 ]]; then
  fail "--yes 는 --apply 와 함께만 사용할 수 있습니다." "--apply --yes 조합으로 다시 실행하거나 기본 dry-run만 수행하세요."
fi

if [[ ${APPLY} -eq 1 && ${ASSUME_YES} -eq 0 ]]; then
  fail "core task start는 interactive prompt를 제공하지 않습니다." "--apply --yes 를 함께 사용하거나 task_start_interactive.sh 를 사용하세요."
fi

python3 scripts/repo/branch_guard.py validate-name --branch "${BRANCH}"

SLUG="${BRANCH#*/}"
TARGET_PATH="${PATH_ROOT}/${SLUG}--${PURPOSE}"
ABS_TARGET_PATH="$(realpath_py "${TARGET_PATH}")"
CURRENT_WORKTREE="$(git rev-parse --show-toplevel 2>/dev/null || true)"
CURRENT_BRANCH="$(git branch --show-current)"
STATUS_LINES="$(git status --short || true)"

if [[ -z "${CURRENT_WORKTREE}" ]]; then
  fail "현재 worktree 경로를 확인할 수 없습니다." "Git worktree 내부에서 다시 실행하세요."
fi

if [[ -e "${TARGET_PATH}" ]]; then
  fail "대상 경로가 이미 존재합니다: ${TARGET_PATH}" "다른 purpose 또는 다른 branch slug로 다시 실행하세요."
fi

BRANCH_EXISTS=0
if git show-ref --verify --quiet "refs/heads/${BRANCH}"; then
  BRANCH_EXISTS=1
fi

if [[ ${BRANCH_EXISTS} -eq 0 ]]; then
  if ! git rev-parse --verify "${BASE}^{commit}" >/dev/null 2>&1; then
    fail "기준 브랜치/커밋을 찾을 수 없습니다: ${BASE}" "--base 값을 올바르게 수정하거나 존재하는 ref를 지정해서 다시 실행하세요."
  fi
fi

WORKTREE_NAME_OUTPUT="$(python3 scripts/repo/worktree_name_guard.py "${TARGET_PATH}" --branch "${BRANCH}" 2>&1)" || {
  echo "${WORKTREE_NAME_OUTPUT}" >&2
  exit 1
}

BRANCH_IN_WORKTREE=0
BRANCH_IN_WORKTREE_PATH=""
WT_PATH=""
ISSUE_URL=""
ISSUE_TITLE=""
ISSUE_STATE=""
ISSUE_STATUS=""
NEXT_ISSUE_STATUS=""
ISSUE_STATUS_LABEL_COUNT=0

while IFS= read -r line; do
  if [[ "${line}" == worktree\ * ]]; then
    WT_PATH="${line#worktree }"
    continue
  fi

  if [[ "${line}" == branch\ refs/heads/* ]]; then
    WT_BRANCH="${line#branch refs/heads/}"
    if [[ "${WT_BRANCH}" == "${BRANCH}" ]]; then
      BRANCH_IN_WORKTREE=1
      BRANCH_IN_WORKTREE_PATH="$(realpath_py "${WT_PATH}")"
      break
    fi
  fi
done < <(git worktree list --porcelain)

if [[ ${BRANCH_IN_WORKTREE} -eq 1 ]]; then
  fail "branch \`${BRANCH}\` 가 이미 checkout 중입니다: ${BRANCH_IN_WORKTREE_PATH}" "기존 worktree로 이동해 작업을 이어가거나 새 branch 이름으로 다시 시작하세요."
fi

if [[ -n "${ISSUE_NUMBER}" ]]; then
  ./scripts/repo/gh_preflight.sh >/dev/null

  ISSUE_VIEW_OUTPUT="$(gh issue view "${ISSUE_NUMBER}" --json number,title,state,labels,url 2>&1)" || {
    fail "issue #${ISSUE_NUMBER} 를 조회할 수 없습니다." "issue 번호와 gh 인증 상태를 확인한 뒤 다시 실행하세요."
  }

  ISSUE_URL="$(extract_issue_field "${ISSUE_VIEW_OUTPUT}" "url")"
  ISSUE_TITLE="$(extract_issue_field "${ISSUE_VIEW_OUTPUT}" "title")"
  ISSUE_STATE="$(extract_issue_field "${ISSUE_VIEW_OUTPUT}" "state")"
  while IFS= read -r status_label; do
    [[ -n "${status_label}" ]] || continue
    ISSUE_STATUS_LABEL_COUNT=$((ISSUE_STATUS_LABEL_COUNT + 1))
    if [[ ${ISSUE_STATUS_LABEL_COUNT} -eq 1 ]]; then
      ISSUE_STATUS="${status_label}"
    fi
  done < <(extract_issue_status_labels "${ISSUE_VIEW_OUTPUT}")

  if [[ "${ISSUE_STATE}" != "OPEN" ]]; then
    fail "issue #${ISSUE_NUMBER} 가 OPEN 상태가 아닙니다: ${ISSUE_STATE}" "열린 issue 번호를 지정하거나 issue 상태를 확인한 뒤 다시 실행하세요."
  fi

  if [[ ${ISSUE_STATUS_LABEL_COUNT} -eq 0 ]]; then
    fail "issue #${ISSUE_NUMBER} 에 status label이 없습니다." "GitHub에서 status:* label 1개를 지정한 뒤 다시 실행하세요."
  fi

  if [[ ${ISSUE_STATUS_LABEL_COUNT} -gt 1 ]]; then
    fail "issue #${ISSUE_NUMBER} 에 status label이 여러 개입니다." "GitHub에서 status:* label을 1개만 남긴 뒤 다시 실행하세요."
  fi

  NEXT_ISSUE_STATUS="status:active"
fi

print_plan() {
  echo "[git-task-start] Dry run"
  echo
  echo "작업 시작 계획을 확인했습니다."
  echo
  echo "- 브랜치: ${BRANCH}"
  if [[ ${BRANCH_EXISTS} -eq 1 ]]; then
    echo "- 기준 브랜치: ${BASE} (기존 branch 재사용으로 미사용)"
  else
    echo "- 기준 브랜치: ${BASE}"
  fi
  echo "- 워크트리 목적: ${PURPOSE}"
  echo "- 생성 예정 경로: ${TARGET_PATH}"
  if [[ -n "${ISSUE_NUMBER}" ]]; then
    echo "- 연결 이슈: #${ISSUE_NUMBER}"
    echo "- 이슈 URL: ${ISSUE_URL}"
    echo "- 현재 이슈 상태: ${ISSUE_STATUS}"
    if [[ "${ISSUE_STATUS}" == "${NEXT_ISSUE_STATUS}" ]]; then
      echo "- apply 시 이슈 상태: ${NEXT_ISSUE_STATUS} (변경 없음)"
    else
      echo "- apply 시 이슈 상태: ${ISSUE_STATUS} -> ${NEXT_ISSUE_STATUS}"
    fi
  fi
  echo
  echo "검증 결과"
  echo "- 브랜치 이름 규칙: 통과"
  echo "- 워크트리 이름 규칙: 통과"
  echo "- 브랜치 사용 가능 여부: 통과"
  if [[ -n "${ISSUE_NUMBER}" ]]; then
    echo "- 이슈 조회/상태 규칙: 통과"
  fi
  echo "- 현재 위치: ${CURRENT_WORKTREE}"
  echo "- 현재 브랜치: ${CURRENT_BRANCH:-HEAD}"
  if [[ -n "${STATUS_LINES}" ]]; then
    echo "- 현재 워크트리 상태: dirty"
    echo "- 참고: 현재 워크트리 변경사항은 유지됩니다."
  else
    echo "- 현재 워크트리 상태: clean"
  fi
  echo
  echo "실행 예정 작업"
  if [[ ${BRANCH_EXISTS} -eq 1 ]]; then
    echo "1. 기존 branch \`${BRANCH}\` 재사용"
  else
    echo "1. ${BASE} 기준으로 branch \`${BRANCH}\` 생성"
  fi
  echo "2. worktree \`${TARGET_PATH}\` 생성"
  echo "3. 대상 worktree에서 branch \`${BRANCH}\` checkout"
  if [[ -n "${ISSUE_NUMBER}" ]]; then
    if [[ "${ISSUE_STATUS}" == "${NEXT_ISSUE_STATUS}" ]]; then
      echo "4. issue #${ISSUE_NUMBER} status 유지 (${NEXT_ISSUE_STATUS})"
    else
      echo "4. issue #${ISSUE_NUMBER} status를 ${NEXT_ISSUE_STATUS} 로 전이"
    fi
  fi
  echo
  echo "실행 예정 명령"
  if [[ ${BRANCH_EXISTS} -eq 0 ]]; then
    echo "- git branch ${BRANCH} ${BASE}"
  fi
  echo "- ./scripts/repo/worktree_add.sh --path ${TARGET_PATH} --branch ${BRANCH}"
  if [[ -n "${ISSUE_NUMBER}" && "${ISSUE_STATUS}" != "${NEXT_ISSUE_STATUS}" ]]; then
    echo "- gh issue edit ${ISSUE_NUMBER} --remove-label ${ISSUE_STATUS} --add-label ${NEXT_ISSUE_STATUS}"
  fi
  if [[ -n "${ISSUE_NUMBER}" ]]; then
    echo "- (cd ${TARGET_PATH} && ./scripts/repo/worktree_issue_metadata.sh write --number ${ISSUE_NUMBER} ...)"
  fi
  echo
  echo "다음 이동 경로"
  echo "- cd ${TARGET_PATH}"
}

print_plan

if [[ ${APPLY} -eq 0 ]]; then
  exit 0
fi

if [[ ${BRANCH_EXISTS} -eq 0 ]]; then
  git branch "${BRANCH}" "${BASE}"
fi

./scripts/repo/worktree_add.sh --path "${TARGET_PATH}" --branch "${BRANCH}"

if [[ -n "${ISSUE_NUMBER}" && "${ISSUE_STATUS}" != "${NEXT_ISSUE_STATUS}" ]]; then
  gh issue edit "${ISSUE_NUMBER}" --remove-label "${ISSUE_STATUS}" --add-label "${NEXT_ISSUE_STATUS}" >/dev/null || {
    fail "branch/worktree 생성 후 issue #${ISSUE_NUMBER} 상태 전이에 실패했습니다." "gh 인증과 issue label 상태를 확인한 뒤 issue status를 수동으로 ${NEXT_ISSUE_STATUS} 로 맞추세요."
  }
fi

if [[ -n "${ISSUE_NUMBER}" ]]; then
  ISSUE_RECORDED_AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  (
    cd "${TARGET_PATH}" &&
    ./scripts/repo/worktree_issue_metadata.sh write \
      --number "${ISSUE_NUMBER}" \
      --url "${ISSUE_URL}" \
      --title "${ISSUE_TITLE}" \
      --status-at-record "${NEXT_ISSUE_STATUS}" \
      --branch "${BRANCH}" \
      --worktree "${ABS_TARGET_PATH}" \
      --recorded-at "${ISSUE_RECORDED_AT}"
  ) >/dev/null || {
    fail "worktree issue metadata 기록에 실패했습니다: ${ABS_TARGET_PATH}" "대상 worktree에서 metadata helper 실행 가능 여부를 확인한 뒤 다시 실행하거나 수동으로 metadata를 정리하세요."
  }
fi

echo
echo "✅ task start 완료"
echo "- 브랜치: ${BRANCH}"
echo "- 워크트리: ${TARGET_PATH}"
if [[ -n "${ISSUE_NUMBER}" ]]; then
  if [[ "${ISSUE_STATUS}" == "${NEXT_ISSUE_STATUS}" ]]; then
    echo "- 이슈: #${ISSUE_NUMBER} (${NEXT_ISSUE_STATUS} 유지)"
  else
    echo "- 이슈: #${ISSUE_NUMBER} (${NEXT_ISSUE_STATUS})"
  fi
fi
echo "- 다음 이동: cd ${TARGET_PATH}"
