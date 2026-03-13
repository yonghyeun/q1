#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../../../.." && pwd)"
cd "${ROOT_DIR}"

MODE="create"
PASSTHROUGH_ARGS=()

while [[ $# -gt 0 ]]; do
  case "${1:-}" in
    --update)
      MODE="update"
      shift
      ;;
    *)
      PASSTHROUGH_ARGS+=("$1")
      shift
      ;;
  esac
done

if [[ "${MODE}" == "update" ]]; then
  ./scripts/repo/pr_update.sh "${PASSTHROUGH_ARGS[@]}"
  exit 0
fi

./scripts/repo/pr_create.sh "${PASSTHROUGH_ARGS[@]}"
