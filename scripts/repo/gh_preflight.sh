#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "${ROOT_DIR}"

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

echo "✅ gh preflight 통과 (origin/gh auth OK)"
