#!/usr/bin/env bash
set -euo pipefail

EXIT_INVALID_INPUT=1
EXIT_INVALID_TITLE=20
EXIT_TYPE_MISMATCH=21

usage() {
  cat <<'EOH'
사용법:
  # 제목 생성
  ./scripts/repo/issue_title_guard.sh generate --type <feature|bug|chore> --summary "<요약>"

  # 제목 검증
  ./scripts/repo/issue_title_guard.sh validate --title "[type] 요약" --type <feature|bug|chore>

설명:
  - 이슈 제목 컨벤션: [type] <요약>
  - 허용 type: feature|bug|chore
EOH
}

is_valid_type() {
  [[ "$1" =~ ^(feature|bug|chore)$ ]]
}

MODE="${1:-}"
if [[ -z "${MODE}" ]]; then
  usage
  exit "${EXIT_INVALID_INPUT}"
fi
shift || true

case "${MODE}" in
  generate)
    TYPE=""
    SUMMARY=""
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --type)
          TYPE="${2:-}"
          shift 2
          ;;
        --summary)
          SUMMARY="${2:-}"
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

    if [[ -z "${TYPE}" || -z "${SUMMARY}" ]]; then
      echo "❌ generate에는 --type, --summary가 필요합니다." >&2
      echo "   다음 행동: feature|bug|chore 중 type을 고르고, 한 줄 요약을 함께 전달." >&2
      exit "${EXIT_INVALID_INPUT}"
    fi

    if ! is_valid_type "${TYPE}"; then
      echo "❌ type 형식이 잘못되었습니다: ${TYPE}" >&2
      echo "   다음 행동: feature|bug|chore 중 하나로 다시 지정." >&2
      exit "${EXIT_INVALID_INPUT}"
    fi

    echo "[${TYPE}] ${SUMMARY}"
    ;;

  validate)
    TYPE=""
    TITLE=""
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

    if [[ -z "${TYPE}" || -z "${TITLE}" ]]; then
      echo "❌ validate에는 --type, --title이 필요합니다." >&2
      echo "   다음 행동: issue type과 [type] 요약 형식 제목을 함께 전달." >&2
      exit "${EXIT_INVALID_INPUT}"
    fi

    if ! is_valid_type "${TYPE}"; then
      echo "❌ type 형식이 잘못되었습니다: ${TYPE}" >&2
      echo "   다음 행동: feature|bug|chore 중 하나로 다시 지정." >&2
      exit "${EXIT_INVALID_INPUT}"
    fi

    if ! [[ "${TITLE}" =~ ^\[([a-z]+)\][[:space:]]+.+$ ]]; then
      echo "❌ 이슈 제목 형식이 정책과 다릅니다: ${TITLE}" >&2
      echo "   허용 형식: [type] 요약" >&2
      echo "   다음 행동: issue-convention.md 형식에 맞춰 [type] 요약으로 수정." >&2
      exit "${EXIT_INVALID_TITLE}"
    fi

    TITLE_TYPE="${BASH_REMATCH[1]}"
    if ! is_valid_type "${TITLE_TYPE}"; then
      echo "❌ 이슈 제목 type 허용값이 아닙니다: ${TITLE_TYPE}" >&2
      echo "   다음 행동: title type을 feature|bug|chore 중 하나로 수정." >&2
      exit "${EXIT_INVALID_TITLE}"
    fi

    if [[ "${TITLE_TYPE}" != "${TYPE}" ]]; then
      echo "❌ 이슈 제목 type과 issue type이 다릅니다: title=${TITLE_TYPE}, type=${TYPE}" >&2
      echo "   다음 행동: 제목 prefix 또는 issue type을 일치시킨 뒤 다시 실행." >&2
      exit "${EXIT_TYPE_MISMATCH}"
    fi

    echo "✅ 이슈 제목 컨벤션 통과: ${TITLE_TYPE}"
    ;;

  *)
    echo "❌ 지원하지 않는 모드입니다: ${MODE}" >&2
    usage
    exit "${EXIT_INVALID_INPUT}"
    ;;
esac
