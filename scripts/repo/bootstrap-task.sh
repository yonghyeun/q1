#!/usr/bin/env bash
set -euo pipefail

TASK_ID="${1:-}"

if [[ -z "${TASK_ID}" ]]; then
  echo "사용법: $0 <TASK_ID>" >&2
  exit 1
fi

if ! [[ "${TASK_ID}" =~ ^T-[0-9]{4}$ ]]; then
  echo "❌ task-id 형식이 잘못되었습니다: ${TASK_ID}" >&2
  exit 1
fi

TASK_DIR="context/tasks/${TASK_ID}"
mkdir -p "${TASK_DIR}"

if [[ ! -f "${TASK_DIR}/context.md" ]]; then
  cat > "${TASK_DIR}/context.md" <<EOC
# ${TASK_ID} Context

## 배경
-

## 제약
-

## 메모
-
EOC
fi

if [[ ! -f "${TASK_DIR}/result.md" ]]; then
  cat > "${TASK_DIR}/result.md" <<EOR
# ${TASK_ID} Result

## 변경 요약
-

## 검증
-

## 후속 조치
-
EOR
fi

echo "${TASK_ID} 컨텍스트 폴더를 초기화했습니다: ${TASK_DIR}"
