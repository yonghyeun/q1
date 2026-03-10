# Gate: branch-name-pre-commit

## Purpose
- 잘못된 branch 이름에서 작업이 진행되는 것을 조기에 차단.
- 보호 브랜치 직접 작업을 차단.

## Trigger
- local `pre-commit`.

## Status
- `active`

## SoT
- [../branch-naming.md](../branch-naming.md)

## Enforcer
- [../../.githooks/pre-commit.d/10-branch-name](../../.githooks/pre-commit.d/10-branch-name)
- [../../scripts/repo/branch_guard.py](../../scripts/repo/branch_guard.py)

## Dependencies
- [../../.githooks/pre-commit.d/10-branch-name](../../.githooks/pre-commit.d/10-branch-name)
- [../../scripts/repo/branch_guard.py](../../scripts/repo/branch_guard.py)

## Failure Mode
- 실패 시 commit 차단.

## Tests
- [../../scripts/repo/tests/test_branch_guard.py](../../scripts/repo/tests/test_branch_guard.py)
