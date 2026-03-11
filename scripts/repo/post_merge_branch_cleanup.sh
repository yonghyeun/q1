#!/usr/bin/env bash
set -euo pipefail

SCRIPT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
ROOT_DIR="${REPO_ROOT_OVERRIDE:-${SCRIPT_ROOT}}"
cd "${ROOT_DIR}"

usage() {
  cat <<'EOF'
사용법:
  ./scripts/repo/post_merge_branch_cleanup.sh --branch <merged-branch> [--base <base-branch>] [--dry-run]

예시:
  ./scripts/repo/post_merge_branch_cleanup.sh --branch feature/signup-flow
  ./scripts/repo/post_merge_branch_cleanup.sh --branch fix/token-race --base main --dry-run
EOF
}

fail() {
  local message="$1"
  local next_action="$2"
  echo "❌ ${message}" >&2
  echo "정책: post-merge branch cleanup은 base 동기화와 merged local branch 삭제만 담당합니다." >&2
  echo "다음 행동: ${next_action}" >&2
  exit 1
}

MERGED_BRANCH=""
BASE_BRANCH="main"
DRY_RUN=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --branch)
      MERGED_BRANCH="${2:-}"
      shift 2
      ;;
    --base)
      BASE_BRANCH="${2:-}"
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

if [[ -z "${MERGED_BRANCH}" ]]; then
  fail "--branch 는 필수입니다." "--branch <merged-branch> 를 명시해서 다시 실행하세요."
fi

if [[ -z "${BASE_BRANCH}" ]]; then
  fail "--base 값이 비어 있습니다." "--base <branch> 를 지정하거나 기본값 main 을 사용하세요."
fi

python3 "${SCRIPT_ROOT}/scripts/repo/dirty_worktree_guard.py" validate-clean

if ! git remote get-url origin >/dev/null 2>&1; then
  fail "origin remote가 없습니다." "git remote add origin <github-repo-url> 후 다시 실행하세요."
fi

CURRENT_BRANCH="$(git branch --show-current || true)"
CURRENT_WORKTREE="$(git rev-parse --show-toplevel 2>/dev/null || true)"

BRANCH_IN_WORKTREE_PATH=""
while IFS= read -r line; do
  if [[ "${line}" == worktree\ * ]]; then
    WT_PATH="${line#worktree }"
    WT_BRANCH=""
    continue
  fi
  if [[ "${line}" == branch\ refs/heads/* ]]; then
    WT_BRANCH="${line#branch refs/heads/}"
    if [[ "${WT_BRANCH}" == "${MERGED_BRANCH}" && "${WT_PATH}" != "${CURRENT_WORKTREE}" ]]; then
      BRANCH_IN_WORKTREE_PATH="${WT_PATH}"
      break
    fi
  fi
done < <(git worktree list --porcelain)

if ! git show-ref --verify --quiet "refs/heads/${BASE_BRANCH}"; then
  fail "base branch가 로컬에 없습니다: ${BASE_BRANCH}" "git fetch origin ${BASE_BRANCH}:${BASE_BRANCH} 후 다시 실행하세요."
fi

if [[ ${DRY_RUN} -eq 1 ]]; then
  echo "✅ dry-run: post-merge branch cleanup 계획"
  echo "- merged branch: ${MERGED_BRANCH}"
  echo "- base branch: ${BASE_BRANCH}"
  if [[ -n "${BRANCH_IN_WORKTREE_PATH}" ]]; then
    echo "- cleanup order precondition: remove linked worktree first (${BRANCH_IN_WORKTREE_PATH})"
  fi
  echo "- switch to ${BASE_BRANCH}"
  echo "- git fetch origin --prune"
  echo "- git pull --rebase origin ${BASE_BRANCH}"
  if git show-ref --verify --quiet "refs/heads/${MERGED_BRANCH}"; then
    echo "- git branch -d ${MERGED_BRANCH}"
  else
    echo "- local branch already absent: ${MERGED_BRANCH}"
  fi
  exit 0
fi

if [[ -n "${BRANCH_IN_WORKTREE_PATH}" ]]; then
  fail "merged branch가 아직 linked worktree에 checkout 중입니다: ${MERGED_BRANCH} @ ${BRANCH_IN_WORKTREE_PATH}" "worktree cleanup을 먼저 수행한 뒤 branch cleanup을 다시 실행하세요."
fi

if [[ "${CURRENT_BRANCH}" != "${BASE_BRANCH}" ]]; then
  git switch "${BASE_BRANCH}"
fi

git fetch origin --prune
if ! git pull --rebase origin "${BASE_BRANCH}"; then
  fail "${BASE_BRANCH} 브랜치 rebase pull에 실패했습니다." "git status 확인 후 필요하면 git rebase --abort 실행, 충돌 해결 뒤 다시 실행하세요."
fi

if git show-ref --verify --quiet "refs/heads/${MERGED_BRANCH}"; then
  if ! git branch -d "${MERGED_BRANCH}"; then
    fail "로컬 브랜치 삭제에 실패했습니다: ${MERGED_BRANCH}" "브랜치가 다른 worktree에서 사용 중인지 확인하고, 정리 후 다시 실행하세요."
  fi
else
  echo "ℹ️ 로컬 브랜치가 이미 없습니다: ${MERGED_BRANCH}"
fi

echo "✅ merge 후 로컬 브랜치 정리 완료: ${MERGED_BRANCH}"
