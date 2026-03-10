# Gate: detached-head-write

## Purpose
- detached HEAD 상태에서 commit, PR 생성, branch 기반 작업이 진행되는 것을 차단.

## Trigger
- write action 직전 sanity check 시점.

## Status
- `active`

## SoT
- [../git-workspace-policy.md](../git-workspace-policy.md)

## Enforcer
- [../../scripts/repo/detached_head_guard.py](../../scripts/repo/detached_head_guard.py)
- [../../.githooks/pre-commit.d/05-detached-head-write](../../.githooks/pre-commit.d/05-detached-head-write)
- [../../.githooks/pre-push](../../.githooks/pre-push)
- [../../scripts/repo/pr_create.sh](../../scripts/repo/pr_create.sh)
- [../../scripts/repo/pr_merge.sh](../../scripts/repo/pr_merge.sh)

## Dependencies
- [../git-workspace-policy.md](../git-workspace-policy.md)

## Failure Mode
- `git rev-parse --abbrev-ref HEAD` 결과가 `HEAD`면 즉시 실패.

## Tests
- [../../scripts/repo/tests/test_detached_head_guard.py](../../scripts/repo/tests/test_detached_head_guard.py)
