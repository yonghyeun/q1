#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "${ROOT_DIR}"

usage() {
  cat <<'EOH'
사용법:
  ./scripts/repo/issue_create.sh --type <feature|bug|chore> --title "<제목>" --body-file <file>

예시:
  ./scripts/repo/issue_create.sh --type feature --title "브랜치 거버넌스 고도화" --body-file /tmp/issue.md
EOH
}

TYPE=""
TITLE=""
BODY_FILE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --type)
      TYPE="${2:-}"
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

if [[ -z "${TYPE}" || -z "${TITLE}" || -z "${BODY_FILE}" ]]; then
  usage
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
./scripts/repo/issue_title_guard.sh validate --type "${TYPE}" --title "${TITLE}"

if [[ ! -f "${BODY_FILE}" ]]; then
  echo "❌ --body-file 파일을 찾을 수 없습니다: ${BODY_FILE}" >&2
  exit 1
fi

python3 scripts/repo/issue_body_quality_guard.py --issue-type "${TYPE}" --body-file "${BODY_FILE}"

ISSUE_URL="$(gh issue create -t "${TITLE}" -F "${BODY_FILE}")"
ISSUE_NUMBER="$(printf '%s' "${ISSUE_URL}" | grep -Eo '[0-9]+$' || true)"

if [[ -z "${ISSUE_NUMBER}" ]]; then
  echo "❌ issue 번호를 추출할 수 없습니다: ${ISSUE_URL}" >&2
  exit 1
fi

echo "✅ Issue 생성 완료"
echo "   - url: ${ISSUE_URL}"
echo "   - number: ${ISSUE_NUMBER}"
