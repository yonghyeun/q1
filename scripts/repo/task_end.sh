#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "${ROOT_DIR}"

usage() {
  cat <<'EOF'
사용법:
  ./scripts/repo/task_end.sh [--pr <number-or-url>] [--branch <branch>] [--worktree <path>] [--method <squash|merge|rebase>] [--subject "<merge-subject>"] [--codex <resume|fork|none>] [--codex-target-worktree <path>] [--apply --yes] [--no-worktree-remove] [--no-branch-cleanup]

예시:
  ./scripts/repo/task_end.sh
  ./scripts/repo/task_end.sh --codex none
  ./scripts/repo/task_end.sh --apply --yes
  ./scripts/repo/task_end.sh --apply --yes --no-worktree-remove
  ./scripts/repo/task_end.sh --pr 42 --worktree ../signup-flow--impl
EOF
}

fail() {
  local message="$1"
  local next_action="$2"
  echo "❌ ${message}" >&2
  echo "정책: task end core는 dry-run이 기본이며, 실제 실행은 --apply --yes로만 수행합니다." >&2
  echo "다음 행동: ${next_action}" >&2
  exit 1
}

realpath_py() {
  python3 -c 'import os,sys; print(os.path.realpath(sys.argv[1]))' "$1"
}

format_codex_followup() {
  local mode="$1"
  local absolute_target_path="$2"
  local thread_id="${CODEX_THREAD_ID:-}"

  if [[ "${mode}" == "none" ]]; then
    echo "- Codex follow-up: disabled (--codex none)"
    return
  fi

  if [[ -z "${thread_id}" ]]; then
    echo "- 현재 환경에서 CODEX_THREAD_ID를 찾지 못했습니다."
    echo "- 자동 재개를 원하면 Codex 안에서 다시 실행하거나 --codex none 으로 비활성화하세요."
    return
  fi

  if [[ "${mode}" == "resume" ]]; then
    echo "- 종료 후 같은 세션을 대상 worktree에서 재개:"
  else
    echo "- 종료 후 새 병렬 세션을 대상 worktree에서 시작:"
  fi
  echo "  codex ${mode} -C ${absolute_target_path} ${thread_id}"
}

exec_codex_followup() {
  local mode="$1"
  local absolute_target_path="$2"
  local thread_id="${CODEX_THREAD_ID:-}"

  if [[ "${mode}" == "none" ]]; then
    return
  fi

  if [[ -z "${thread_id}" ]]; then
    fail "자동 Codex ${mode} 실행에 필요한 CODEX_THREAD_ID를 찾을 수 없습니다." "Codex 안에서 다시 실행하거나 --codex none 으로 비활성화하세요."
  fi

  if ! command -v codex >/dev/null 2>&1; then
    fail "\`codex\` 명령을 찾을 수 없습니다." "Codex CLI를 설치했는지 확인하거나 --codex none 으로 비활성화하세요."
  fi

  cd "${absolute_target_path}"
  exec codex "${mode}" -C "${absolute_target_path}" "${thread_id}"
}

run_worktree_cleanup() {
  if [[ "${WORKTREE}" == "${CURRENT_WORKTREE}" && "${WORKTREE}" != "${PRIMARY_WORKTREE}" ]]; then
    (cd "${PRIMARY_WORKTREE}" && ./scripts/repo/worktree_cleanup.sh "$@")
    return
  fi

  ./scripts/repo/worktree_cleanup.sh "$@"
}

run_branch_cleanup() {
  if [[ "${PRIMARY_WORKTREE}" != "${CURRENT_WORKTREE}" ]]; then
    (cd "${PRIMARY_WORKTREE}" && ./scripts/repo/post_merge_branch_cleanup.sh "$@")
    return
  fi

  ./scripts/repo/post_merge_branch_cleanup.sh "$@"
}

METHOD="squash"
PR_TARGET=""
BRANCH=""
WORKTREE=""
SUBJECT=""
APPLY=0
ASSUME_YES=0
NO_WORKTREE_REMOVE=0
NO_BRANCH_CLEANUP=0
CODEX_MODE="resume"
CODEX_TARGET_WORKTREE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --pr)
      PR_TARGET="${2:-}"
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
    --method)
      METHOD="${2:-}"
      shift 2
      ;;
    --subject)
      SUBJECT="${2:-}"
      shift 2
      ;;
    --codex)
      CODEX_MODE="${2:-}"
      shift 2
      ;;
    --codex-target-worktree)
      CODEX_TARGET_WORKTREE="${2:-}"
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
    --no-worktree-remove)
      NO_WORKTREE_REMOVE=1
      shift
      ;;
    --no-branch-cleanup)
      NO_BRANCH_CLEANUP=1
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

case "${METHOD}" in
  squash|merge|rebase) ;;
  *)
    fail "--method 는 squash|merge|rebase 중 하나여야 합니다." "--method 값을 squash, merge, rebase 중 하나로 수정해서 다시 실행하세요."
    ;;
esac

case "${CODEX_MODE}" in
  resume|fork|none) ;;
  *)
    fail "--codex 는 resume|fork|none 중 하나여야 합니다." "--codex 값을 허용된 값 중 하나로 수정해서 다시 실행하세요."
    ;;
esac

if [[ ${ASSUME_YES} -eq 1 && ${APPLY} -eq 0 ]]; then
  fail "--yes 는 --apply 와 함께만 사용할 수 있습니다." "--apply --yes 조합으로 다시 실행하거나 기본 dry-run만 수행하세요."
fi

if [[ ${APPLY} -eq 1 && ${ASSUME_YES} -eq 0 ]]; then
  fail "core task end는 interactive prompt를 제공하지 않습니다." "--apply --yes 를 함께 사용하거나 task_end_interactive.sh 를 사용하세요."
fi

python3 scripts/repo/detached_head_guard.py validate-write
python3 scripts/repo/dirty_worktree_guard.py validate-clean

CURRENT_BRANCH="$(git branch --show-current)"
if [[ -z "${CURRENT_BRANCH}" ]]; then
  fail "현재 브랜치를 확인할 수 없습니다." "브랜치가 checkout된 worktree에서 다시 실행하거나 --branch 를 명시하세요."
fi

CURRENT_WORKTREE="$(git rev-parse --show-toplevel 2>/dev/null || true)"
if [[ -z "${CURRENT_WORKTREE}" ]]; then
  fail "현재 worktree 경로를 확인할 수 없습니다." "Git worktree 내부에서 실행하거나 --worktree 로 대상 경로를 명시하세요."
fi

PRIMARY_WORKTREE="$(git worktree list --porcelain | awk '/^worktree /{print substr($0,10); exit}')"
if [[ -z "${PRIMARY_WORKTREE}" ]]; then
  fail "primary worktree 경로를 확인할 수 없습니다." "git worktree list 결과를 확인한 뒤 다시 실행하세요."
fi

BRANCH="${BRANCH:-${CURRENT_BRANCH}}"
WORKTREE="${WORKTREE:-${CURRENT_WORKTREE}}"
PR_VIEW_TARGET="${PR_TARGET:-${BRANCH}}"
CODEX_TARGET_WORKTREE="${CODEX_TARGET_WORKTREE:-${PRIMARY_WORKTREE}}"
ABS_CODEX_TARGET_WORKTREE="$(realpath_py "${CODEX_TARGET_WORKTREE}")"

if [[ "${CODEX_MODE}" != "none" && ! -d "${ABS_CODEX_TARGET_WORKTREE}" ]]; then
  fail "Codex target worktree 경로를 찾을 수 없습니다: ${CODEX_TARGET_WORKTREE}" "--codex-target-worktree 를 올바른 경로로 지정하거나 --codex none 으로 비활성화하세요."
fi

if [[ "${CODEX_MODE}" != "none" && ${NO_WORKTREE_REMOVE} -eq 0 && "$(realpath_py "${WORKTREE}")" == "${ABS_CODEX_TARGET_WORKTREE}" ]]; then
  fail "Codex target worktree가 종료 중 제거될 worktree와 같습니다: ${CODEX_TARGET_WORKTREE}" "--codex-target-worktree 를 다른 경로로 지정하거나 --no-worktree-remove 또는 --codex none 으로 다시 실행하세요."
fi

PR_LABEL="${PR_VIEW_TARGET}"
PR_NUMBER=""
PR_TITLE=""

if [[ ${APPLY} -eq 1 ]]; then
  ./scripts/repo/gh_preflight.sh >/dev/null
  PR_NUMBER="$(gh pr view "${PR_VIEW_TARGET}" --json number --jq .number 2>/dev/null || true)"
  if [[ -z "${PR_NUMBER}" || "${PR_NUMBER}" == "null" ]]; then
    fail "현재 문맥에서 merge 대상 PR을 자동 추론할 수 없습니다." "--pr <number-or-url> 를 명시해서 다시 실행하세요."
  fi
  PR_LABEL="#${PR_NUMBER}"
  PR_TITLE="$(gh pr view "${PR_NUMBER}" --json title --jq .title 2>/dev/null || true)"
  if [[ -z "${PR_TITLE}" || "${PR_TITLE}" == "null" ]]; then
    fail "PR 제목을 조회할 수 없습니다: #${PR_NUMBER}" "--subject 를 명시하거나 gh auth 상태를 확인한 뒤 다시 실행하세요."
  fi
fi

MERGE_SUBJECT="${SUBJECT}"
if [[ -z "${MERGE_SUBJECT}" && "${METHOD}" != "rebase" ]]; then
  if [[ -n "${PR_TITLE}" ]]; then
    MERGE_SUBJECT="${PR_TITLE}"
  else
    MERGE_SUBJECT="<PR_TITLE_FROM_GH>"
  fi
fi

MERGE_DRY_ARGS=(--method "${METHOD}" --dry-run)
MERGE_RUN_ARGS=(--method "${METHOD}")
if [[ -n "${PR_TARGET}" ]]; then
  MERGE_DRY_ARGS+=(--pr "${PR_TARGET}")
  MERGE_RUN_ARGS+=(--pr "${PR_TARGET}")
fi
if [[ -n "${MERGE_SUBJECT}" && "${METHOD}" != "rebase" ]]; then
  MERGE_DRY_ARGS+=(--subject "${MERGE_SUBJECT}")
  MERGE_RUN_ARGS+=(--subject "${MERGE_SUBJECT}")
fi

BRANCH_CLEANUP_DRY_ARGS=(--branch "${BRANCH}" --dry-run)
BRANCH_CLEANUP_RUN_ARGS=(--branch "${BRANCH}")

WORKTREE_DRY_ARGS=(--worktree "${WORKTREE}" --expected-branch "${BRANCH}" --dry-run)
WORKTREE_RUN_ARGS=(--worktree "${WORKTREE}" --expected-branch "${BRANCH}")

MERGE_PLAN_OUTPUT="$(./scripts/repo/pr_merge.sh "${MERGE_DRY_ARGS[@]}" 2>&1)" || {
  echo "${MERGE_PLAN_OUTPUT}" >&2
  fail "merge dry-run 검증에 실패했습니다." "위 실패 메시지의 다음 행동을 먼저 수행한 뒤 다시 실행하세요."
}

BRANCH_CLEANUP_OUTPUT=""
if [[ ${NO_BRANCH_CLEANUP} -eq 0 ]]; then
  BRANCH_CLEANUP_OUTPUT="$(run_branch_cleanup "${BRANCH_CLEANUP_DRY_ARGS[@]}" 2>&1)" || {
    echo "${BRANCH_CLEANUP_OUTPUT}" >&2
    fail "branch cleanup dry-run 검증에 실패했습니다." "위 실패 메시지의 다음 행동을 먼저 수행한 뒤 다시 실행하세요."
  }
fi

WORKTREE_CLEANUP_OUTPUT=""
if [[ ${NO_WORKTREE_REMOVE} -eq 0 ]]; then
  WORKTREE_CLEANUP_OUTPUT="$(run_worktree_cleanup "${WORKTREE_DRY_ARGS[@]}" 2>&1)" || {
    echo "${WORKTREE_CLEANUP_OUTPUT}" >&2
    fail "worktree cleanup dry-run 검증에 실패했습니다." "위 실패 메시지의 다음 행동을 먼저 수행한 뒤 다시 실행하세요."
  }
fi

echo "✅ dry-run: task end 계획"
echo "- PR: ${PR_LABEL}"
echo "- Branch: ${BRANCH}"
echo "- Worktree: ${WORKTREE}"
echo "- Method: ${METHOD}"
if [[ -n "${MERGE_SUBJECT}" ]]; then
echo "- Merge subject: ${MERGE_SUBJECT}"
else
  echo "- Merge subject: <not-used>"
fi
echo "- Branch cleanup: $([[ ${NO_BRANCH_CLEANUP} -eq 1 ]] && echo skip || echo run)"
echo "- Worktree cleanup: $([[ ${NO_WORKTREE_REMOVE} -eq 1 ]] && echo skip || echo run)"
echo "- Codex target worktree: ${ABS_CODEX_TARGET_WORKTREE}"
echo
echo "[merge]"
echo "${MERGE_PLAN_OUTPUT}"
if [[ -n "${BRANCH_CLEANUP_OUTPUT}" ]]; then
  echo
  echo "[branch cleanup]"
  echo "${BRANCH_CLEANUP_OUTPUT}"
fi
if [[ -n "${WORKTREE_CLEANUP_OUTPUT}" ]]; then
  echo
  echo "[worktree cleanup]"
  echo "${WORKTREE_CLEANUP_OUTPUT}"
fi
echo
echo "Codex 세션 이어가기"
format_codex_followup "${CODEX_MODE}" "${ABS_CODEX_TARGET_WORKTREE}"

if [[ ${APPLY} -eq 0 ]]; then
  exit 0
fi

./scripts/repo/pr_merge.sh "${MERGE_RUN_ARGS[@]}"

if [[ ${NO_WORKTREE_REMOVE} -eq 0 ]]; then
  run_worktree_cleanup "${WORKTREE_RUN_ARGS[@]}"
fi

if [[ ${NO_BRANCH_CLEANUP} -eq 0 ]]; then
  run_branch_cleanup "${BRANCH_CLEANUP_RUN_ARGS[@]}"
fi

echo "✅ task end 완료: ${PR_LABEL}"
echo "- 다음 Codex worktree: ${ABS_CODEX_TARGET_WORKTREE}"
format_codex_followup "${CODEX_MODE}" "${ABS_CODEX_TARGET_WORKTREE}"

exec_codex_followup "${CODEX_MODE}" "${ABS_CODEX_TARGET_WORKTREE}"
