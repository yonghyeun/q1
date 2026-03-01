#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "${ROOT_DIR}"

usage() {
  cat <<'EOF'
사용법:
  ./scripts/repo/start_task_from_issue.sh \
    --task-id <T-000N> \
    --issue <number> \
    --slug <short-topic>

예시:
  ./scripts/repo/start_task_from_issue.sh --task-id T-0001 --issue 1234 --slug branch-governance
EOF
}

TASK_ID=""
ISSUE_NUMBER=""
SLUG=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --task-id)
      TASK_ID="${2:-}"
      shift 2
      ;;
    --issue)
      ISSUE_NUMBER="${2:-}"
      shift 2
      ;;
    --slug)
      SLUG="${2:-}"
      shift 2
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

if [[ -z "${TASK_ID}" || -z "${ISSUE_NUMBER}" || -z "${SLUG}" ]]; then
  usage
  exit 1
fi

if ! [[ "${TASK_ID}" =~ ^T-[0-9]{4}$ ]]; then
  echo "❌ task-id 형식이 잘못되었습니다: ${TASK_ID}" >&2
  exit 1
fi

if ! [[ "${ISSUE_NUMBER}" =~ ^[0-9]+$ ]]; then
  echo "❌ issue 번호 형식이 잘못되었습니다: ${ISSUE_NUMBER}" >&2
  exit 1
fi

if ! [[ "${SLUG}" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
  echo "❌ slug 형식이 잘못되었습니다: ${SLUG}" >&2
  exit 1
fi

BRANCH="task/i${ISSUE_NUMBER}-${TASK_ID}-${SLUG}"

if ! git remote get-url origin >/dev/null 2>&1; then
  echo "❌ origin remote가 없습니다." >&2
  echo "   예시: git remote add origin <github-repo-url>" >&2
  exit 1
fi

git switch main
git pull --ff-only
git switch -c "${BRANCH}"
./scripts/repo/bootstrap-task.sh "${TASK_ID}"
python3 scripts/repo/branch_guard.py validate-name
python3 scripts/repo/branch_guard.py validate-context

echo "✅ 작업 시작 준비 완료"
echo "   - branch: ${BRANCH}"
echo "   - task dir: agent-team/runs/${TASK_ID}"
