#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "${ROOT_DIR}"

extract_json_field() {
  local json_input="$1"
  local field_name="$2"
  python3 -c '
import json
import sys

data = json.loads(sys.argv[1])
field = sys.argv[2]
value = data.get(field, "")
if value is None:
    value = ""
print(value)
' "${json_input}" "${field_name}"
}

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

python3 scripts/repo/detached_head_guard.py validate-write
python3 scripts/repo/protected_branch_write_guard.py validate-write --branch "${BRANCH}"
python3 scripts/repo/branch_guard.py validate-name --branch "${BRANCH}"
python3 scripts/repo/dirty_worktree_guard.py validate-clean

./scripts/repo/pr_title_guard.sh validate --title "${TITLE}" --branch "${BRANCH}"

if [[ ! -f "${BODY_FILE}" ]]; then
  echo "❌ --body-file 파일을 찾을 수 없습니다: ${BODY_FILE}" >&2
  exit 1
fi

python3 scripts/repo/pr_body_quality_guard.py --body-file "${BODY_FILE}"
python3 scripts/repo/pr_issue_guard.py --pr-body-file "${BODY_FILE}"

if [[ ${DRY_RUN} -eq 0 ]]; then
  ./scripts/repo/gh_preflight.sh --require-api
fi

if [[ ${DRY_RUN} -eq 1 ]]; then
  echo "✅ dry-run: PR 생성 명령"
  echo "gh pr create --base ${BASE} --head ${BRANCH} --title \"${TITLE}\" --body-file \"${BODY_FILE}\" $([[ ${DRAFT} -eq 1 ]] && echo '--draft')"
  exit 0
fi

CREATE_ARGS=(pr create --base "${BASE}" --head "${BRANCH}" --title "${TITLE}" --body-file "${BODY_FILE}")
if [[ ${DRAFT} -eq 1 ]]; then
  CREATE_ARGS+=(--draft)
fi

CREATE_OUTPUT="$(gh "${CREATE_ARGS[@]}")"
PR_URL="$(printf '%s\n' "${CREATE_OUTPUT}" | tail -n 1)"
PR_NUMBER="$(printf '%s' "${PR_URL}" | grep -Eo '[0-9]+$' || true)"

if [[ -z "${PR_NUMBER}" ]]; then
  echo "❌ PR 번호를 추출할 수 없습니다: ${PR_URL}" >&2
  exit 1
fi

PR_JSON="$(gh pr view "${PR_NUMBER}" --json number,title,url,state,baseRefName,headRefName 2>/dev/null || true)"

METADATA_URL="${PR_URL}"
METADATA_TITLE="${TITLE}"
METADATA_STATE=""
METADATA_BASE_BRANCH="${BASE}"
METADATA_HEAD_BRANCH="${BRANCH}"

if [[ -n "${PR_JSON}" ]]; then
  METADATA_URL="$(extract_json_field "${PR_JSON}" "url")"
  METADATA_TITLE="$(extract_json_field "${PR_JSON}" "title")"
  METADATA_STATE="$(extract_json_field "${PR_JSON}" "state")"
  METADATA_BASE_BRANCH="$(extract_json_field "${PR_JSON}" "baseRefName")"
  METADATA_HEAD_BRANCH="$(extract_json_field "${PR_JSON}" "headRefName")"
fi

RECORDED_AT="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
./scripts/repo/worktree_pr_metadata.sh write \
  --number "${PR_NUMBER}" \
  --url "${METADATA_URL}" \
  --title "${METADATA_TITLE}" \
  --state "${METADATA_STATE}" \
  --base-branch "${METADATA_BASE_BRANCH}" \
  --head-branch "${METADATA_HEAD_BRANCH}" \
  --worktree "${ROOT_DIR}" \
  --recorded-at "${RECORDED_AT}" >/dev/null || {
  echo "❌ PR metadata 기록에 실패했습니다: #${PR_NUMBER}" >&2
  echo "다음 행동: 현재 worktree에서 worktree_pr_metadata.sh write 경로를 확인한 뒤 PR metadata를 수동 기록하세요." >&2
  exit 1
}

echo "✅ PR 생성 완료: branch=${BRANCH}"
echo "   - url: ${METADATA_URL}"
echo "   - number: ${PR_NUMBER}"
