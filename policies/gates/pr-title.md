# Gate: pr-title

## Purpose
- PR 제목이 `[scope] 요약` 형식을 따르는지 검증.
- 필요 시 현재 branch scope와 제목 scope 일치 여부를 검증.

## Trigger
- `scripts/repo/pr_create.sh` 실행 직전.

## Status
- `active`

## SoT
- [../branch-pr-convention.md](../branch-pr-convention.md)
- [../branch-naming.md](../branch-naming.md)

## Enforcer
- [../../scripts/repo/pr_title_guard.sh](../../scripts/repo/pr_title_guard.sh)

## Dependencies
- [../../scripts/repo/pr_create.sh](../../scripts/repo/pr_create.sh)
- [../../scripts/repo/branch_guard.py](../../scripts/repo/branch_guard.py)
- [../branch-pr-convention.md](../branch-pr-convention.md)

## Failure Mode
- 실패 시 PR 생성 차단.

## Tests
- [../../scripts/repo/tests/test_pr_title_guard.py](../../scripts/repo/tests/test_pr_title_guard.py)
