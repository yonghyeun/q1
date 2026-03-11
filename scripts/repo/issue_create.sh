#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "${ROOT_DIR}"

usage() {
  cat <<'EOH'
사용법:
  ./scripts/repo/issue_create.sh --type <feature|bug|chore> --status <inbox|ready|active|blocked|cancelled> --priority <p0|p1|p2|p3> --source-type <human-request|agent-team|runtime-observation|wbs-planned> --area <product|repo|docs|agent-team> [--area <product|repo|docs|agent-team> ...] --title "<제목>" --body-file <file>

예시:
  ./scripts/repo/issue_create.sh --type feature --status inbox --priority p2 --source-type human-request --area repo --title "[feature] 브랜치 거버넌스 고도화" --body-file /tmp/issue.md
EOH
}

TYPE=""
STATUS=""
PRIORITY=""
SOURCE_TYPE=""
TITLE=""
BODY_FILE=""
AREAS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --type)
      TYPE="${2:-}"
      shift 2
      ;;
    --status)
      STATUS="${2:-}"
      shift 2
      ;;
    --priority)
      PRIORITY="${2:-}"
      shift 2
      ;;
    --source-type)
      SOURCE_TYPE="${2:-}"
      shift 2
      ;;
    --area)
      AREAS+=("${2:-}")
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

if [[ -z "${TYPE}" || -z "${STATUS}" || -z "${PRIORITY}" || -z "${SOURCE_TYPE}" || -z "${TITLE}" || -z "${BODY_FILE}" || ${#AREAS[@]} -eq 0 ]]; then
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

./scripts/repo/issue_title_guard.sh validate --type "${TYPE}" --title "${TITLE}"

if [[ ! -f "${BODY_FILE}" ]]; then
  echo "❌ --body-file 파일을 찾을 수 없습니다: ${BODY_FILE}" >&2
  exit 1
fi

python3 scripts/repo/issue_body_quality_guard.py --issue-type "${TYPE}" --body-file "${BODY_FILE}"
AREA_ARGS=()
for area in "${AREAS[@]}"; do
  AREA_ARGS+=("--area" "${area}")
done

LABEL_ARGS=()
while IFS= read -r label; do
  [[ -n "${label}" ]] || continue
  LABEL_ARGS+=("--label" "${label}")
done < <(
  python3 scripts/repo/issue_label_guard.py \
    --type "${TYPE}" \
    --status "${STATUS}" \
    --priority "${PRIORITY}" \
    --source-type "${SOURCE_TYPE}" \
    "${AREA_ARGS[@]}"
)

./scripts/repo/gh_preflight.sh --require-api

ISSUE_URL="$(gh issue create -t "${TITLE}" -F "${BODY_FILE}" "${LABEL_ARGS[@]}")"
ISSUE_NUMBER="$(printf '%s' "${ISSUE_URL}" | grep -Eo '[0-9]+$' || true)"

if [[ -z "${ISSUE_NUMBER}" ]]; then
  echo "❌ issue 번호를 추출할 수 없습니다: ${ISSUE_URL}" >&2
  exit 1
fi

echo "✅ Issue 생성 완료"
echo "   - url: ${ISSUE_URL}"
echo "   - number: ${ISSUE_NUMBER}"
