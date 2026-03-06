#!/usr/bin/env bash
set -euo pipefail

EXIT_INVALID_INPUT=1

usage() {
  cat <<'EOH'
사용법:
  ./scripts/repo/codex_wbs_emit.sh <kind> --prompt-file <path> --output-file <path> [--profile <name>] [--model <name>]

kind:
  - handoff-packet
  - trace-summary
  - run-ledger

설명:
  - Codex를 non-interactive 모드로 실행하고 `--output-schema`로 structured output을 강제합니다.
  - 생성 직후 `validate_wbs_artifact.py`로 schema + semantic 검증을 수행합니다.
EOH
}

if [[ $# -lt 1 ]]; then
  usage
  exit "${EXIT_INVALID_INPUT}"
fi

KIND="${1:-}"
shift || true

PROMPT_FILE=""
OUTPUT_FILE=""
PROFILE=""
MODEL=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --prompt-file)
      PROMPT_FILE="${2:-}"
      shift 2
      ;;
    --output-file)
      OUTPUT_FILE="${2:-}"
      shift 2
      ;;
    --profile)
      PROFILE="${2:-}"
      shift 2
      ;;
    --model)
      MODEL="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "❌ 알 수 없는 옵션: $1" >&2
      usage
      exit "${EXIT_INVALID_INPUT}"
      ;;
  esac
done

if [[ -z "${PROMPT_FILE}" || -z "${OUTPUT_FILE}" ]]; then
  echo "❌ --prompt-file 과 --output-file 이 필요합니다." >&2
  exit "${EXIT_INVALID_INPUT}"
fi

if [[ ! -f "${PROMPT_FILE}" ]]; then
  echo "❌ prompt 파일을 찾을 수 없습니다: ${PROMPT_FILE}" >&2
  exit "${EXIT_INVALID_INPUT}"
fi

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

case "${KIND}" in
  handoff-packet)
    SCHEMA_REL="context/wbs/schemas/handoff-packet.schema.json"
    ;;
  trace-summary)
    SCHEMA_REL="context/wbs/schemas/trace-summary.schema.json"
    ;;
  run-ledger)
    SCHEMA_REL="context/wbs/schemas/run-ledger.schema.json"
    ;;
  *)
    echo "❌ 지원하지 않는 kind 입니다: ${KIND}" >&2
    usage
    exit "${EXIT_INVALID_INPUT}"
    ;;
esac

SCHEMA_PATH="${REPO_ROOT}/${SCHEMA_REL}"
mkdir -p "$(dirname "${OUTPUT_FILE}")"

CMD=(codex exec --cd "${REPO_ROOT}" --output-schema "${SCHEMA_PATH}" -o "${OUTPUT_FILE}")

if [[ -n "${PROFILE}" ]]; then
  CMD+=(-p "${PROFILE}")
fi

if [[ -n "${MODEL}" ]]; then
  CMD+=(-m "${MODEL}")
fi

CMD+=(-)

"${CMD[@]}" < "${PROMPT_FILE}"

python3 "${REPO_ROOT}/scripts/repo/validate_wbs_artifact.py" --kind "${KIND}" --file "${OUTPUT_FILE}"
echo "✅ structured artifact generated: ${KIND} -> ${OUTPUT_FILE}"
