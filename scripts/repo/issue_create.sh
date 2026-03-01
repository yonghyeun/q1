#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "${ROOT_DIR}"

usage() {
  cat <<'EOF'
사용법:
  ./scripts/repo/issue_create.sh --type <feature|bug|chore> --task-id <T-000N> --title "<제목>" --body-file <file>

예시:
  ./scripts/repo/issue_create.sh --type feature --task-id T-0001 --title "브랜치 거버넌스 고도화" --body-file /tmp/issue.md
EOF
}

TYPE=""
TASK_ID=""
TITLE=""
BODY_FILE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --type)
      TYPE="${2:-}"
      shift 2
      ;;
    --task-id)
      TASK_ID="${2:-}"
      shift 2
      ;;
    --title)
      TITLE="${2:-}"
      shift 2
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

if [[ -z "${TYPE}" || -z "${TASK_ID}" || -z "${TITLE}" || -z "${BODY_FILE}" ]]; then
  usage
  exit 1
fi

if ! [[ "${TASK_ID}" =~ ^T-[0-9]{4}$ ]]; then
  echo "❌ task-id 형식이 잘못되었습니다: ${TASK_ID}" >&2
  exit 1
fi

case "${TYPE}" in
  feature|bug|chore)
    ;;
  *)
    echo "❌ --type 은 feature|bug|chore 중 하나여야 합니다." >&2
    exit 1
    ;;
esac

./scripts/repo/gh_preflight.sh

FULL_TITLE="[${TASK_ID}] ${TITLE}"
if [[ ! -f "${BODY_FILE}" ]]; then
  echo "❌ --body-file 파일을 찾을 수 없습니다: ${BODY_FILE}" >&2
  exit 1
fi

python3 scripts/repo/body_quality_guard.py \
  --kind issue \
  --issue-type "${TYPE}" \
  --body-file "${BODY_FILE}"

ISSUE_URL="$(gh issue create -t "${FULL_TITLE}" -F "${BODY_FILE}")"

ISSUE_NUMBER="$(printf '%s' "${ISSUE_URL}" | grep -Eo '[0-9]+$' || true)"

if [[ -z "${ISSUE_NUMBER}" ]]; then
  echo "❌ issue 번호를 추출할 수 없습니다: ${ISSUE_URL}" >&2
  exit 1
fi

echo "✅ Issue 생성 완료"
echo "   - url: ${ISSUE_URL}"
echo "   - number: ${ISSUE_NUMBER}"
