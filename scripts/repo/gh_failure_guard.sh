#!/usr/bin/env bash
set -euo pipefail

gh_output_indicates_connectivity_issue() {
  local output="${1:-}"
  [[ "${output}" == *"api.github.com"* || "${output}" == *"error connecting"* || "${output}" == *"dial tcp"* || "${output}" == *"i/o timeout"* || "${output}" == *"connection refused"* ]]
}

gh_connectivity_suffix() {
  echo "sandbox/network에서 api.github.com 접근이 차단된 상태일 수 있습니다."
}

gh_retry_next_action() {
  echo "같은 wrapper 명령을 권한 상승으로 재실행하세요."
}

gh_print_output_hint() {
  local output="${1:-}"
  local first_line=""
  first_line="$(printf '%s\n' "${output}" | head -n 1)"
  [[ -n "${first_line}" ]] || return 0
  echo "   gh 출력: ${first_line}" >&2
}
