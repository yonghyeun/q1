#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "${ROOT_DIR}"

usage() {
  cat <<'EOF'
사용법:
  ./scripts/repo/gh_preflight.sh [--require-api]
EOF
}

REQUIRE_API=0
while [[ $# -gt 0 ]]; do
  case "${1:-}" in
    --require-api)
      REQUIRE_API=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "❌ 알 수 없는 옵션: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if ! git remote get-url origin >/dev/null 2>&1; then
  echo "❌ origin remote가 없습니다." >&2
  echo "   예시: git remote add origin <github-repo-url>" >&2
  exit 1
fi

if ! gh auth status -h github.com >/dev/null 2>&1; then
  echo "❌ gh 인증이 유효하지 않습니다." >&2
  echo "   실행: gh auth login -h github.com" >&2
  exit 1
fi

if [[ ${REQUIRE_API} -eq 1 ]]; then
  API_OUTPUT="$(gh api rate_limit --jq '.resources.core.limit' 2>&1)" || {
    echo "❌ GitHub API 연결 확인에 실패했습니다." >&2
    if [[ "${API_OUTPUT}" == *"api.github.com"* || "${API_OUTPUT}" == *"error connecting"* || "${API_OUTPUT}" == *"dial tcp"* || "${API_OUTPUT}" == *"i/o timeout"* ]]; then
      echo "   현재 sandbox/network에서 api.github.com 접근이 차단된 상태일 수 있습니다." >&2
      echo "   이 경우 저장소 wrapper 문제라기보다 실행 환경 제약일 가능성이 큽니다." >&2
      echo "   다음 행동: 같은 wrapper 명령을 권한 상승으로 재실행하세요." >&2
    else
      echo "   gh api 출력: ${API_OUTPUT}" >&2
      echo "   다음 행동: GitHub API 접근 상태와 gh 인증을 확인한 뒤 다시 실행하세요." >&2
    fi
    exit 1
  }
fi

if [[ ${REQUIRE_API} -eq 1 ]]; then
  echo "✅ gh preflight 통과 (origin/gh auth/API OK)"
else
  echo "✅ gh preflight 통과 (origin/gh auth OK)"
fi
