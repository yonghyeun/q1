# Gate: issue-title

## Purpose
- issue 제목이 `[type] 요약` 형식을 따르는지 검증.
- issue type과 제목 prefix가 일치하는지 검증.

## Trigger
- `scripts/repo/issue_create.sh` 실행 직전.

## Status
- `active`

## SoT
- [../issue-convention.md](../issue-convention.md)

## Enforcer
- [../../scripts/repo/issue_title_guard.sh](../../scripts/repo/issue_title_guard.sh)

## Dependencies
- [../issue-convention.md](../issue-convention.md)
- [../../scripts/repo/issue_create.sh](../../scripts/repo/issue_create.sh)

## Failure Mode
- 실패 시 issue 생성 차단.

## Tests
- [../../scripts/repo/tests/test_issue_title_guard.py](../../scripts/repo/tests/test_issue_title_guard.py)
