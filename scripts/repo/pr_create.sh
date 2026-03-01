#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "${ROOT_DIR}"

usage() {
  cat <<'EOF'
사용법:
  ./scripts/repo/pr_create.sh --title "<PR 제목>" [--base main] [--draft] [--body-file <file>] [--dry-run]

예시:
  ./scripts/repo/pr_create.sh --title "[T-0001] 브랜치 정책 고도화"
  ./scripts/repo/pr_create.sh --title "[T-0001] 브랜치 정책 고도화" --draft
EOF
}

TITLE=""
BASE="main"
DRAFT=0
DRY_RUN=0
BODY_FILE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --title)
      TITLE="${2:-}"
      shift 2
      ;;
    --base)
      BASE="${2:-}"
      shift 2
      ;;
    --draft)
      DRAFT=1
      shift
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    --body-file)
      BODY_FILE="${2:-}"
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

if [[ -z "${TITLE}" ]]; then
  echo "❌ --title 은 필수입니다." >&2
  usage
  exit 1
fi

BRANCH="$(git branch --show-current)"
if [[ -z "${BRANCH}" ]]; then
  echo "❌ 현재 브랜치를 확인할 수 없습니다." >&2
  exit 1
fi

if [[ "${BRANCH}" =~ ^task/i([0-9]+)-(T-[0-9]{4})-([a-z0-9-]+)$ ]]; then
  ISSUE_NUMBER="${BASH_REMATCH[1]}"
  TASK_ID="${BASH_REMATCH[2]}"
else
  echo "❌ 브랜치 형식이 정책과 다릅니다: ${BRANCH}" >&2
  exit 1
fi

./scripts/repo/gh_preflight.sh
python3 scripts/repo/branch_guard.py validate-name --branch "${BRANCH}"
python3 scripts/repo/branch_guard.py validate-context --branch "${BRANCH}"
python3 scripts/repo/branch_guard.py validate-pr --branch "${BRANCH}"

TEMP_BODY_FILE=""
if [[ -n "${BODY_FILE}" ]]; then
  if [[ ! -f "${BODY_FILE}" ]]; then
    echo "❌ --body-file 파일을 찾을 수 없습니다: ${BODY_FILE}" >&2
    exit 1
  fi
  USE_BODY_FILE="${BODY_FILE}"
else
  TEMP_BODY_FILE="$(mktemp)"
  cat > "${TEMP_BODY_FILE}" <<EOF
Closes #${ISSUE_NUMBER}

## 목적 (Why)
- ${TASK_ID} 작업 반영

## 변경 요약 (What)
- 브랜치: ${BRANCH}
- runs: agent-team/runs/${TASK_ID}/
EOF
  USE_BODY_FILE="${TEMP_BODY_FILE}"
fi

python3 scripts/repo/pr_issue_guard.py --branch "${BRANCH}" --pr-body-file "${USE_BODY_FILE}"

if [[ ${DRY_RUN} -eq 1 ]]; then
  echo "✅ dry-run: PR 생성 명령"
  echo "gh pr create --base ${BASE} --head ${BRANCH} --title \"${TITLE}\" --body-file \"${USE_BODY_FILE}\" $([[ ${DRAFT} -eq 1 ]] && echo '--draft')"
  if [[ -n "${TEMP_BODY_FILE}" ]]; then
    rm -f "${TEMP_BODY_FILE}"
  fi
  exit 0
fi

CREATE_ARGS=(pr create --base "${BASE}" --head "${BRANCH}" --title "${TITLE}" --body-file "${USE_BODY_FILE}")
if [[ ${DRAFT} -eq 1 ]]; then
  CREATE_ARGS+=(--draft)
fi

gh "${CREATE_ARGS[@]}"
echo "✅ PR 생성 완료: branch=${BRANCH}, issue=#${ISSUE_NUMBER}"

if [[ -n "${TEMP_BODY_FILE}" ]]; then
  rm -f "${TEMP_BODY_FILE}"
fi
