#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "${ROOT_DIR}"
source "${ROOT_DIR}/scripts/repo/gh_failure_guard.sh"

extract_json_field() {
  local json_input="$1"
  local field_path="$2"
  python3 -c '
import json
import sys

data = json.loads(sys.argv[1])
value = data
for key in sys.argv[2].split("."):
    if isinstance(value, dict):
        value = value.get(key, "")
    else:
        value = ""
    if value is None:
        value = ""
if isinstance(value, bool):
    print("true" if value else "false")
else:
    print(value)
' "${json_input}" "${field_path}"
}

extract_repo_slug() {
  local origin_url
  origin_url="$(git remote get-url origin 2>/dev/null || true)"
  python3 -c '
import re
import sys

origin = sys.argv[1].strip()
match = re.search(r"github\.com[:/]([^/]+)/([^/]+?)(?:\.git)?$", origin)
if not match:
    sys.exit(1)
print(f"{match.group(1)}/{match.group(2)}")
' "${origin_url}"
}

get_recorded_pr_number() {
  local metadata_output
  metadata_output="$(./scripts/repo/worktree_pr_metadata.sh read)"
  printf '%s\n' "${metadata_output}" | sed -n 's/^q1\.pr\.number=//p' | head -n 1
}

usage() {
  cat <<'EOH'
사용법:
  ./scripts/repo/pr_update.sh --title "<PR 제목>" --body-file <file> [--number <n>] [--dry-run]

예시:
  ./scripts/repo/pr_update.sh --title "[config] PR 수정 경로 정리" --body-file /tmp/pr.md
  ./scripts/repo/pr_update.sh --number 41 --title "[config] PR 수정 경로 정리" --body-file /tmp/pr.md
EOH
}

TITLE=""
DRY_RUN=0
BODY_FILE=""
PR_NUMBER=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --title)
      TITLE="${2:-}"
      shift 2
      ;;
    --body-file)
      BODY_FILE="${2:-}"
      shift 2
      ;;
    --number)
      PR_NUMBER="${2:-}"
      shift 2
      ;;
    --dry-run)
      DRY_RUN=1
      shift
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

if [[ ! -f "${BODY_FILE}" ]]; then
  echo "❌ --body-file 파일을 찾을 수 없습니다: ${BODY_FILE}" >&2
  exit 1
fi

if [[ -z "${PR_NUMBER}" ]]; then
  PR_NUMBER="$(get_recorded_pr_number)"
fi

if [[ -z "${PR_NUMBER}" ]]; then
  echo "❌ 수정 대상 PR 번호를 확인할 수 없습니다." >&2
  echo "다음 행동: --number 로 PR 번호를 지정하거나 현재 worktree의 PR metadata를 먼저 기록하세요." >&2
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
python3 scripts/repo/pr_body_quality_guard.py --body-file "${BODY_FILE}"
python3 scripts/repo/pr_issue_guard.py --pr-body-file "${BODY_FILE}"

if [[ ${DRY_RUN} -eq 0 ]]; then
  ./scripts/repo/gh_preflight.sh --require-api
fi

REPO_SLUG="$(extract_repo_slug 2>/dev/null || true)"
if [[ -z "${REPO_SLUG}" ]]; then
  echo "❌ origin remote에서 GitHub 저장소 경로를 추출할 수 없습니다." >&2
  echo "다음 행동: origin remote URL이 github.com 저장소를 가리키는지 확인한 뒤 다시 실행하세요." >&2
  exit 1
fi

API_ENDPOINT="repos/${REPO_SLUG}/pulls/${PR_NUMBER}"

if [[ ${DRY_RUN} -eq 1 ]]; then
  echo "✅ dry-run: PR 수정 명령"
  echo "gh api -X PATCH ${API_ENDPOINT} --input <json-with-title-and-body>"
  exit 0
fi

PAYLOAD_FILE="$(mktemp)"
trap 'rm -f "${PAYLOAD_FILE}"' EXIT

python3 - "${TITLE}" "${BODY_FILE}" "${PAYLOAD_FILE}" <<'PY'
import json
import pathlib
import sys

title = sys.argv[1]
body_path = pathlib.Path(sys.argv[2])
payload_path = pathlib.Path(sys.argv[3])

payload = {
    "title": title,
    "body": body_path.read_text(encoding="utf-8"),
}
payload_path.write_text(json.dumps(payload), encoding="utf-8")
PY

PATCH_OUTPUT="$(gh api -X PATCH "${API_ENDPOINT}" --input "${PAYLOAD_FILE}" 2>&1)" || {
  if gh_output_indicates_connectivity_issue "${PATCH_OUTPUT}"; then
    echo "❌ PR 수정에 실패했습니다. $(gh_connectivity_suffix)" >&2
    echo "다음 행동: $(gh_retry_next_action)" >&2
  else
    echo "❌ PR 수정에 실패했습니다." >&2
    gh_print_output_hint "${PATCH_OUTPUT}"
    echo "다음 행동: PR 번호, GitHub 권한, gh 상태를 확인한 뒤 같은 wrapper 명령을 다시 실행하세요." >&2
  fi
  exit 1
}

METADATA_URL="$(extract_json_field "${PATCH_OUTPUT}" "html_url")"
METADATA_TITLE="$(extract_json_field "${PATCH_OUTPUT}" "title")"
METADATA_STATE="$(extract_json_field "${PATCH_OUTPUT}" "state")"
METADATA_BASE_BRANCH="$(extract_json_field "${PATCH_OUTPUT}" "base.ref")"
METADATA_HEAD_BRANCH="$(extract_json_field "${PATCH_OUTPUT}" "head.ref")"

if [[ -z "${METADATA_URL}" ]]; then
  echo "❌ PR 수정 응답에서 PR URL을 확인할 수 없습니다." >&2
  echo "다음 행동: gh api 응답 형식을 확인한 뒤 같은 wrapper 명령을 다시 실행하세요." >&2
  exit 1
fi

if [[ -z "${METADATA_HEAD_BRANCH}" ]]; then
  METADATA_HEAD_BRANCH="${BRANCH}"
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
  --recorded-at "${RECORDED_AT}" \
  --recorded-by "pr_update" >/dev/null || {
  echo "❌ PR metadata 기록에 실패했습니다: #${PR_NUMBER}" >&2
  echo "다음 행동: 현재 worktree에서 worktree_pr_metadata.sh write 경로를 확인한 뒤 PR metadata를 수동 기록하세요." >&2
  exit 1
}

echo "✅ PR 수정 완료: #${PR_NUMBER}"
echo "   - url: ${METADATA_URL}"
echo "   - title: ${METADATA_TITLE}"
