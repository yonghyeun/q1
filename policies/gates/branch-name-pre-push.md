# Gate: branch-name-pre-push

## Purpose
- 잘못된 branch 이름의 push를 차단.
- 보호 브랜치 직접 push를 차단.

## Trigger
- local `pre-push`.

## Status
- `active`

## SoT
- [../branch-naming.md](../branch-naming.md)

## Enforcer
- [../../.githooks/pre-push](../../.githooks/pre-push)
- [../../scripts/repo/branch_guard.py](../../scripts/repo/branch_guard.py)

## Dependencies
- [../../.githooks/pre-push](../../.githooks/pre-push)
- [../../scripts/repo/branch_guard.py](../../scripts/repo/branch_guard.py)

## Failure Mode
- 실패 시 push 차단.

## Tests
- [../../scripts/repo/tests/test_branch_guard.py](../../scripts/repo/tests/test_branch_guard.py)
