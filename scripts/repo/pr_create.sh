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

if [[ ${DRY_RUN} -eq 0 ]]; then
  ./scripts/repo/gh_preflight.sh
fi
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
## Issue Link (Required)
Closes #${ISSUE_NUMBER}

## 목적 (Why)
- ${TASK_ID} 작업 반영 및 이슈 #${ISSUE_NUMBER} 해결

## 변경 요약 (What)
- 브랜치: ${BRANCH}
- runs: agent-team/runs/${TASK_ID}/

## 범위
### In Scope
- ${TASK_ID} 범위 산출물 반영
- 브랜치/PR 정책 게이트 통과

### Out of Scope
- 후속 태스크에서 처리할 별도 기능 변경

## 영향도 / 리스크
- 영향 범위: 브랜치 ${BRANCH} 기준 변경 파일 일체
- 잠재 리스크:
  - 정책/템플릿 변경 시 본문과 검증 조건 불일치 가능
- 완화 방안:
  - PR 생성 전 branch/pr guard를 재검증

## 리뷰 포인트 (Reviewer Focus)
- 이슈 링크(Closes #${ISSUE_NUMBER})와 브랜치 issue 번호 일치 여부
- task 컨텍스트(\`agent-team/runs/${TASK_ID}/\`) 산출물 충족 여부

## 수동 검증 (선택)
- 필요한 경우 검증 명령과 결과를 기입

## 참고 링크
- Task ID: \`${TASK_ID}\`
- runs: \`agent-team/runs/${TASK_ID}/\`
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
