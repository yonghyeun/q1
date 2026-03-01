#!/usr/bin/env bash
set -euo pipefail

TASK_ID="${1:-}"

if [[ -z "${TASK_ID}" ]]; then
  echo "사용법: $0 <TASK_ID>" >&2
  exit 1
fi

mkdir -p "agent-team/runs/${TASK_ID}"
echo "{\"task_id\": \"${TASK_ID}\", \"status\": \"created\"}" > "agent-team/runs/${TASK_ID}/status.json"

echo "${TASK_ID} 실행 폴더를 초기화했습니다."
