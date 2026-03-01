#!/usr/bin/env bash
set -euo pipefail

EXIT_INVALID_INPUT=1
EXIT_INVALID_TITLE=10
EXIT_BRANCH_PARSE_FAIL=11
EXIT_TASK_MISMATCH=12

usage() {
  cat <<'EOF'
사용법:
  # 제목 생성
  ./scripts/repo/pr_title_guard.sh generate --task-id <T-000N> --summary "<요약>"

  # 제목 검증
  ./scripts/repo/pr_title_guard.sh validate --title "[T-000N] 요약" [--branch task/i123-T-000N-topic]

설명:
  - PR 제목 컨벤션: [T-000N] <요약>
  - --branch를 주면 브랜치의 task-id와 제목 task-id 일치 여부까지 검증합니다.
EOF
}

MODE="${1:-}"
if [[ -z "${MODE}" ]]; then
  usage
  exit "${EXIT_INVALID_INPUT}"
fi
shift || true

case "${MODE}" in
  generate)
    TASK_ID=""
    SUMMARY=""
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --task-id)
          TASK_ID="${2:-}"
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

    if [[ -z "${TASK_ID}" || -z "${SUMMARY}" ]]; then
      echo "❌ generate에는 --task-id, --summary가 필요합니다." >&2
      exit "${EXIT_INVALID_INPUT}"
    fi
    if ! [[ "${TASK_ID}" =~ ^T-[0-9]{4}$ ]]; then
      echo "❌ task-id 형식이 잘못되었습니다: ${TASK_ID}" >&2
      exit "${EXIT_INVALID_INPUT}"
    fi
    echo "[${TASK_ID}] ${SUMMARY}"
    ;;

  validate)
    TITLE=""
    BRANCH=""
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --title)
          TITLE="${2:-}"
          shift 2
          ;;
        --branch)
          BRANCH="${2:-}"
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

    if [[ -z "${TITLE}" ]]; then
      echo "❌ validate에는 --title이 필요합니다." >&2
      exit "${EXIT_INVALID_INPUT}"
    fi

    if ! [[ "${TITLE}" =~ ^\[(T-[0-9]{4})\][[:space:]]+.+$ ]]; then
      echo "❌ PR 제목 형식이 정책과 다릅니다: ${TITLE}" >&2
      echo "   허용 형식: [T-000N] 요약" >&2
      exit "${EXIT_INVALID_TITLE}"
    fi
    TITLE_TASK_ID="${BASH_REMATCH[1]}"

    if [[ -n "${BRANCH}" ]]; then
      if [[ "${BRANCH}" =~ (T-[0-9]{4}) ]]; then
        BRANCH_TASK_ID="${BASH_REMATCH[1]}"
      else
        echo "❌ 브랜치에서 task-id를 찾을 수 없습니다: ${BRANCH}" >&2
        exit "${EXIT_BRANCH_PARSE_FAIL}"
      fi

      if [[ "${TITLE_TASK_ID}" != "${BRANCH_TASK_ID}" ]]; then
        echo "❌ PR 제목 task-id와 브랜치 task-id가 다릅니다: title=${TITLE_TASK_ID}, branch=${BRANCH_TASK_ID}" >&2
        exit "${EXIT_TASK_MISMATCH}"
      fi
    fi

    echo "✅ PR 제목 컨벤션 통과: ${TITLE_TASK_ID}"
    ;;

  *)
    echo "❌ 지원하지 않는 모드입니다: ${MODE}" >&2
    usage
    exit "${EXIT_INVALID_INPUT}"
    ;;
esac
