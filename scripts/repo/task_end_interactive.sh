#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "${ROOT_DIR}"

for arg in "$@"; do
  case "${arg}" in
    --apply|--yes)
      echo "❌ task_end_interactive.sh 는 --apply 또는 --yes 를 직접 받지 않습니다." >&2
      echo "정책: interactive wrapper는 먼저 dry-run을 수행하고, 확인 후 core를 --apply --yes로 재실행합니다." >&2
      echo "다음 행동: 해당 옵션을 제거하고 다시 실행하세요." >&2
      exit 1
      ;;
  esac
done

./scripts/repo/task_end.sh "$@"

printf "Proceed? [y/N] "
read -r answer
if [[ "${answer}" != "y" && "${answer}" != "Y" ]]; then
  echo "ℹ️ task end를 취소했습니다."
  exit 0
fi

./scripts/repo/task_end.sh "$@" --apply --yes
