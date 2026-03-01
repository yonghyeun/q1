#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "${ROOT_DIR}"

usage() {
  cat <<'EOF'
사용법:
  ./scripts/repo/issue_create.sh --type <feature|bug|chore> --task-id <T-000N> --title "<제목>"

예시:
  ./scripts/repo/issue_create.sh --type feature --task-id T-0001 --title "브랜치 거버넌스 고도화"
EOF
}

TYPE=""
TASK_ID=""
TITLE=""

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

if [[ -z "${TYPE}" || -z "${TASK_ID}" || -z "${TITLE}" ]]; then
  usage
  exit 1
fi

if ! [[ "${TASK_ID}" =~ ^T-[0-9]{4}$ ]]; then
  echo "❌ task-id 형식이 잘못되었습니다: ${TASK_ID}" >&2
  exit 1
fi

case "${TYPE}" in
  feature)
    TEMPLATE_FILE="feature.md"
    ;;
  bug)
    TEMPLATE_FILE="bug.md"
    ;;
  chore)
    TEMPLATE_FILE="chore.md"
    ;;
  *)
    echo "❌ --type 은 feature|bug|chore 중 하나여야 합니다." >&2
    exit 1
    ;;
esac

./scripts/repo/gh_preflight.sh

FULL_TITLE="[${TASK_ID}] ${TITLE}"
TEMPLATE_PATH=".github/ISSUE_TEMPLATE/${TEMPLATE_FILE}"
if [[ ! -f "${TEMPLATE_PATH}" ]]; then
  echo "❌ 이슈 템플릿 파일을 찾을 수 없습니다: ${TEMPLATE_PATH}" >&2
  exit 1
fi

TEMP_BODY_FILE="$(mktemp)"
awk '
  BEGIN { sep=0 }
  /^---$/ { sep++; next }
  sep >= 2 { print }
' "${TEMPLATE_PATH}" > "${TEMP_BODY_FILE}"

python3 - "${TEMP_BODY_FILE}" "${TASK_ID}" <<'PY'
from pathlib import Path
import sys

body_path = Path(sys.argv[1])
task_id = sys.argv[2]
body = body_path.read_text(encoding="utf-8")
body = body.replace("T-000N", task_id)
body_path.write_text(body, encoding="utf-8")
PY

ISSUE_URL="$(gh issue create -t "${FULL_TITLE}" -F "${TEMP_BODY_FILE}")"
rm -f "${TEMP_BODY_FILE}"

ISSUE_NUMBER="$(printf '%s' "${ISSUE_URL}" | grep -Eo '[0-9]+$' || true)"

if [[ -z "${ISSUE_NUMBER}" ]]; then
  echo "❌ issue 번호를 추출할 수 없습니다: ${ISSUE_URL}" >&2
  exit 1
fi

echo "✅ Issue 생성 완료"
echo "   - url: ${ISSUE_URL}"
echo "   - number: ${ISSUE_NUMBER}"
