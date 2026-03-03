#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "${ROOT_DIR}"

usage() {
  cat <<'EOH'
사용법:
  ./scripts/repo/pr_create.sh --title "<PR 제목>" --body-file <file> [--base main] [--draft] [--dry-run]

예시:
  ./scripts/repo/pr_create.sh --title "[config] 브랜치 정책 정리" --body-file /tmp/pr.md
  ./scripts/repo/pr_create.sh --title "[config] 브랜치 정책 정리" --body-file /tmp/pr.md --draft
EOH
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

if [[ -z "${TITLE}" || -z "${BODY_FILE}" ]]; then
  echo "❌ --title, --body-file 은 필수입니다." >&2
  usage
  exit 1
fi

BRANCH="$(git branch --show-current)"
if [[ -z "${BRANCH}" ]]; then
  echo "❌ 현재 브랜치를 확인할 수 없습니다." >&2
  exit 1
fi

./scripts/repo/pr_title_guard.sh validate --title "${TITLE}" --branch "${BRANCH}"

if [[ ${DRY_RUN} -eq 0 ]]; then
  ./scripts/repo/gh_preflight.sh
fi

python3 scripts/repo/branch_guard.py validate-name --branch "${BRANCH}"
python3 scripts/repo/branch_guard.py validate-context --branch "${BRANCH}"
python3 scripts/repo/branch_guard.py validate-pr --branch "${BRANCH}"

if [[ ! -f "${BODY_FILE}" ]]; then
  echo "❌ --body-file 파일을 찾을 수 없습니다: ${BODY_FILE}" >&2
  exit 1
fi

python3 scripts/repo/body_quality_guard.py --kind pr --body-file "${BODY_FILE}"
python3 scripts/repo/pr_issue_guard.py --pr-body-file "${BODY_FILE}"

if [[ ${DRY_RUN} -eq 1 ]]; then
  echo "✅ dry-run: PR 생성 명령"
  echo "gh pr create --base ${BASE} --head ${BRANCH} --title \"${TITLE}\" --body-file \"${BODY_FILE}\" $([[ ${DRAFT} -eq 1 ]] && echo '--draft')"
  exit 0
fi

CREATE_ARGS=(pr create --base "${BASE}" --head "${BRANCH}" --title "${TITLE}" --body-file "${BODY_FILE}")
if [[ ${DRAFT} -eq 1 ]]; then
  CREATE_ARGS+=(--draft)
fi

gh "${CREATE_ARGS[@]}"
echo "✅ PR 생성 완료: branch=${BRANCH}"
