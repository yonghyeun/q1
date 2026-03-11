#!/usr/bin/env bash
set -euo pipefail

EXIT_INVALID_INPUT=1
EXIT_NOT_ENABLED=10

usage() {
  cat <<'EOF'
사용법:
  ./scripts/repo/worktree_config_bootstrap.sh validate
  ./scripts/repo/worktree_config_bootstrap.sh ensure

설명:
  - linked worktree에서 `git config --worktree` 를 쓰기 위한 repo 설정을 검증/보정한다.
  - 대상 설정: `extensions.worktreeConfig=true`
EOF
}

MODE="${1:-}"
if [[ -z "${MODE}" ]]; then
  usage
  exit "${EXIT_INVALID_INPUT}"
fi
shift || true

if [[ $# -gt 0 ]]; then
  echo "❌ 알 수 없는 옵션: $*" >&2
  usage
  exit "${EXIT_INVALID_INPUT}"
fi

CURRENT_VALUE="$(git config --get --bool extensions.worktreeConfig || true)"

case "${MODE}" in
  validate)
    if [[ "${CURRENT_VALUE}" == "true" ]]; then
      echo "✅ worktree config bootstrap 통과: extensions.worktreeConfig=true"
      exit 0
    fi

    echo "❌ extensions.worktreeConfig 가 활성화되지 않았습니다." >&2
    echo "다음 행동: ./scripts/repo/worktree_config_bootstrap.sh ensure 로 bootstrap을 수행하세요." >&2
    exit "${EXIT_NOT_ENABLED}"
    ;;

  ensure)
    if [[ "${CURRENT_VALUE}" == "true" ]]; then
      echo "✅ worktree config bootstrap 이미 활성화됨"
      exit 0
    fi

    git config extensions.worktreeConfig true
    echo "✅ worktree config bootstrap 완료: extensions.worktreeConfig=true"
    ;;

  -h|--help)
    usage
    ;;

  *)
    echo "❌ 지원하지 않는 모드입니다: ${MODE}" >&2
    usage
    exit "${EXIT_INVALID_INPUT}"
    ;;
esac
