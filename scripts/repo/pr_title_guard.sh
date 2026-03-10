#!/usr/bin/env bash
set -euo pipefail

EXIT_INVALID_INPUT=1
EXIT_INVALID_TITLE=10
EXIT_BRANCH_PARSE_FAIL=11
EXIT_SCOPE_MISMATCH=12

usage() {
  cat <<'EOH'
사용법:
  # 제목 생성
  ./scripts/repo/pr_title_guard.sh generate --scope <scope> --summary "<요약>"

  # 제목 검증
  ./scripts/repo/pr_title_guard.sh validate --title "[scope] 요약" [--branch config/topic]

설명:
  - PR 제목 컨벤션: [scope] <요약>
  - 허용 scope: feature|fix|docs|config|chore|refactor|hotfix
  - --branch를 주면 브랜치 prefix와 제목 scope 일치 여부를 검증합니다.
EOH
}

is_valid_scope() {
  [[ "$1" =~ ^(feature|fix|docs|config|chore|refactor|hotfix)$ ]]
}

MODE="${1:-}"
if [[ -z "${MODE}" ]]; then
  usage
  exit "${EXIT_INVALID_INPUT}"
fi
shift || true

case "${MODE}" in
  generate)
    SCOPE=""
    SUMMARY=""
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --scope)
          SCOPE="${2:-}"
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

    if [[ -z "${SCOPE}" || -z "${SUMMARY}" ]]; then
      echo "❌ generate에는 --scope, --summary가 필요합니다." >&2
      echo "   다음 행동: 허용 scope와 한 줄 summary를 함께 전달." >&2
      exit "${EXIT_INVALID_INPUT}"
    fi

    if ! is_valid_scope "${SCOPE}"; then
      echo "❌ scope 형식이 잘못되었습니다: ${SCOPE}" >&2
      echo "   다음 행동: feature|fix|docs|config|chore|refactor|hotfix 중 하나로 수정." >&2
      exit "${EXIT_INVALID_INPUT}"
    fi

    echo "[${SCOPE}] ${SUMMARY}"
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
      echo "   다음 행동: [scope] 요약 형식의 PR 제목을 전달." >&2
      exit "${EXIT_INVALID_INPUT}"
    fi

    if ! [[ "${TITLE}" =~ ^\[([a-z]+)\][[:space:]]+.+$ ]]; then
      echo "❌ PR 제목 형식이 정책과 다릅니다: ${TITLE}" >&2
      echo "   허용 형식: [scope] 요약" >&2
      echo "   다음 행동: branch-pr-convention.md 형식에 맞춰 [scope] 요약으로 수정." >&2
      exit "${EXIT_INVALID_TITLE}"
    fi

    TITLE_SCOPE="${BASH_REMATCH[1]}"
    if ! is_valid_scope "${TITLE_SCOPE}"; then
      echo "❌ PR 제목 scope 허용값이 아닙니다: ${TITLE_SCOPE}" >&2
      echo "   다음 행동: title scope를 허용 scope 목록 중 하나로 수정." >&2
      exit "${EXIT_INVALID_TITLE}"
    fi

    if [[ -n "${BRANCH}" ]]; then
      if [[ "${BRANCH}" =~ ^([a-z]+)/ ]]; then
        BRANCH_SCOPE="${BASH_REMATCH[1]}"
      else
        echo "❌ 브랜치에서 scope를 찾을 수 없습니다: ${BRANCH}" >&2
        echo "   다음 행동: <scope>/<slug> 형식 브랜치에서 다시 실행." >&2
        exit "${EXIT_BRANCH_PARSE_FAIL}"
      fi

      if [[ "${TITLE_SCOPE}" != "${BRANCH_SCOPE}" ]]; then
        echo "❌ PR 제목 scope와 브랜치 scope가 다릅니다: title=${TITLE_SCOPE}, branch=${BRANCH_SCOPE}" >&2
        echo "   다음 행동: 제목 scope 또는 브랜치 scope를 일치시킨 뒤 다시 실행." >&2
        exit "${EXIT_SCOPE_MISMATCH}"
      fi
    fi

    echo "✅ PR 제목 컨벤션 통과: ${TITLE_SCOPE}"
    ;;

  *)
    echo "❌ 지원하지 않는 모드입니다: ${MODE}" >&2
    usage
    exit "${EXIT_INVALID_INPUT}"
    ;;
esac
