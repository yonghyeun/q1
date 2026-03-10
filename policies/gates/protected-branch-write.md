# Gate: protected-branch-write

## Purpose
- 보호 브랜치에서의 직접 쓰기 작업을 차단.
- `main` branch 직접 commit, push, PR-less write를 예방.

## Trigger
- commit 전, push 전, write helper 실행 직전 sanity check 시점.

## Status
- `active`

## SoT
- [../git-workspace-policy.md](../git-workspace-policy.md)
- [../branch-naming.md](../branch-naming.md)

## Enforcer
- [../../scripts/repo/protected_branch_write_guard.py](../../scripts/repo/protected_branch_write_guard.py)
- [../../.githooks/pre-commit.d/15-protected-branch-write](../../.githooks/pre-commit.d/15-protected-branch-write)
- [../../.githooks/pre-push](../../.githooks/pre-push)
- [../../scripts/repo/pr_create.sh](../../scripts/repo/pr_create.sh)
- [../../scripts/repo/pr_merge.sh](../../scripts/repo/pr_merge.sh)
- branch naming과 분리된 보호 브랜치 write 전용 sanity check 담당.

## Dependencies
- [../git-workspace-policy.md](../git-workspace-policy.md)

## Failure Mode
- 보호 브랜치 감지 시 즉시 실패.

## Tests
- [../../scripts/repo/tests/test_protected_branch_write_guard.py](../../scripts/repo/tests/test_protected_branch_write_guard.py)
