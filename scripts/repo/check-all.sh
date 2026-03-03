#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"

# shellcheck source=../lib/common.sh
source "${ROOT_DIR}/scripts/lib/common.sh"

log_info "저장소 기본 점검을 시작합니다."

REQUIRED_PATHS=(
  "apps/web"
  "docs"
  "context"
  "policies"
)

for p in "${REQUIRED_PATHS[@]}"; do
  if [[ ! -e "${ROOT_DIR}/${p}" ]]; then
    log_error "필수 경로 누락: ${p}"
    exit 1
  fi
  log_info "확인 완료: ${p}"
done

log_info "기본 점검을 완료했습니다."
