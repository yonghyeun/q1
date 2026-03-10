#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "${ROOT_DIR}"

usage() {
  cat <<'EOF'
사용법:
  ./scripts/repo/worktree_add.sh --path <worktree-path> [--branch <branch>] [--dry-run] [-- <git-worktree-add-extra-args>...]

예시:
  ./scripts/repo/worktree_add.sh --path ../signup-flow--impl --branch feature/signup-flow
  ./scripts/repo/worktree_add.sh --path ../signup-flow--review --dry-run -- --track -b feature/signup-flow-review
EOF
}

TARGET_PATH=""
BRANCH=""
DRY_RUN=0
EXTRA_ARGS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --path)
      TARGET_PATH="${2:-}"
      shift 2
      ;;
    --branch)
      BRANCH="${2:-}"
      shift 2
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    --)
      shift
      EXTRA_ARGS=("$@")
      break
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

if [[ -z "${TARGET_PATH}" ]]; then
  echo "❌ --path 는 필수입니다." >&2
  usage
  exit 1
fi

GUARD_ARGS=("${TARGET_PATH}")
if [[ -n "${BRANCH}" ]]; then
  GUARD_ARGS+=(--branch "${BRANCH}")
fi

python3 scripts/repo/worktree_name_guard.py "${GUARD_ARGS[@]}"

CMD=(git worktree add "${TARGET_PATH}")
if [[ -n "${BRANCH}" ]]; then
  CMD+=("${BRANCH}")
fi
if [[ ${#EXTRA_ARGS[@]} -gt 0 ]]; then
  CMD+=("${EXTRA_ARGS[@]}")
fi

if [[ ${DRY_RUN} -eq 1 ]]; then
  PRINT_CMD=""
  for arg in "${CMD[@]}"; do
    PRINT_CMD+=" $(printf '%q' "${arg}")"
  done
  echo "✅ dry-run: worktree add 명령"
  echo "${PRINT_CMD# }"
  exit 0
fi

"${CMD[@]}"

echo "✅ worktree 생성 완료: ${TARGET_PATH}"
