#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "${ROOT_DIR}"

usage() {
  cat <<'EOF'
사용법:
  ./scripts/repo/worktree_cleanup.sh --worktree <path> [--expected-branch <branch>] [--dry-run]

예시:
  ./scripts/repo/worktree_cleanup.sh --worktree ../signup-flow--impl --expected-branch feature/signup-flow
  ./scripts/repo/worktree_cleanup.sh --worktree ../signup-flow--review --dry-run
EOF
}

fail() {
  local message="$1"
  local next_action="$2"
  echo "❌ ${message}" >&2
  echo "정책: worktree cleanup은 removable 상태가 확인된 linked worktree만 제거합니다." >&2
  echo "다음 행동: ${next_action}" >&2
  exit 1
}

TARGET_PATH=""
EXPECTED_BRANCH=""
DRY_RUN=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --worktree)
      TARGET_PATH="${2:-}"
      shift 2
      ;;
    --expected-branch)
      EXPECTED_BRANCH="${2:-}"
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
      fail "알 수 없는 옵션: $1" "사용법을 확인한 뒤 다시 실행하세요."
      ;;
  esac
done

if [[ -z "${TARGET_PATH}" ]]; then
  fail "--worktree 는 필수입니다." "--worktree <path> 를 명시해서 다시 실행하세요."
fi

if ! TARGET_REALPATH="$(python3 -c 'import os, sys; print(os.path.realpath(sys.argv[1]))' "${TARGET_PATH}")"; then
  fail "worktree 경로를 확인할 수 없습니다: ${TARGET_PATH}" "경로가 올바른지 확인한 뒤 다시 실행하세요."
fi

if [[ ! -d "${TARGET_REALPATH}" ]]; then
  fail "worktree 경로가 존재하지 않습니다: ${TARGET_REALPATH}" "실제 worktree 경로를 확인한 뒤 다시 실행하세요."
fi

if [[ -d "${TARGET_REALPATH}/.git" ]]; then
  fail "primary worktree는 자동 제거하지 않습니다: ${TARGET_REALPATH}" "linked worktree 경로를 지정하거나 --no-worktree-remove 로 최종화를 진행하세요."
fi

if ! git -C "${TARGET_REALPATH}" rev-parse --show-toplevel >/dev/null 2>&1; then
  fail "git worktree가 아닌 경로입니다: ${TARGET_REALPATH}" "git worktree list 로 경로를 확인한 뒤 다시 실행하세요."
fi

TARGET_TOPLEVEL="$(git -C "${TARGET_REALPATH}" rev-parse --show-toplevel)"
if [[ "${TARGET_TOPLEVEL}" != "${TARGET_REALPATH}" ]]; then
  fail "입력 경로가 worktree 루트가 아닙니다: ${TARGET_REALPATH}" "git worktree list 로 표시된 루트 경로를 그대로 사용하세요."
fi

CURRENT_TOPLEVEL="$(git rev-parse --show-toplevel)"
if [[ "${CURRENT_TOPLEVEL}" == "${TARGET_REALPATH}" ]]; then
  fail "현재 활성 worktree는 직접 제거하지 않습니다: ${TARGET_REALPATH}" "다른 worktree로 이동한 뒤 다시 실행하거나 task_end.sh 가 primary worktree로 이동하도록 하세요."
fi

if [[ -n "$(git -C "${TARGET_REALPATH}" status --porcelain)" ]]; then
  fail "대상 worktree에 미커밋 변경사항이 있습니다: ${TARGET_REALPATH}" "변경사항을 커밋하거나 정리한 뒤 다시 실행하세요."
fi

TARGET_BRANCH="$(git -C "${TARGET_REALPATH}" branch --show-current)"
if [[ -z "${TARGET_BRANCH}" ]]; then
  fail "대상 worktree가 detached HEAD 상태입니다: ${TARGET_REALPATH}" "브랜치를 명확히 checkout 하거나 수동 정리 후 다시 실행하세요."
fi

if [[ -n "${EXPECTED_BRANCH}" && "${TARGET_BRANCH}" != "${EXPECTED_BRANCH}" ]]; then
  fail "대상 worktree 브랜치가 예상과 다릅니다. actual=${TARGET_BRANCH}, expected=${EXPECTED_BRANCH}" "기대 브랜치를 다시 확인하거나 --expected-branch 값을 수정해서 다시 실행하세요."
fi

if [[ ${DRY_RUN} -eq 1 ]]; then
  echo "✅ dry-run: worktree cleanup 계획"
  echo "- worktree: ${TARGET_REALPATH}"
  echo "- branch: ${TARGET_BRANCH}"
  echo "- git worktree remove ${TARGET_REALPATH}"
  echo "- git worktree prune"
  exit 0
fi

if ! git worktree remove "${TARGET_REALPATH}"; then
  fail "worktree 제거에 실패했습니다: ${TARGET_REALPATH}" "worktree가 다른 프로세스에서 사용 중인지 확인하고 상태를 정리한 뒤 다시 실행하세요."
fi

git worktree prune

echo "✅ worktree 정리 완료: ${TARGET_REALPATH}"
