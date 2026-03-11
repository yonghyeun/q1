# Gate: issue-label

## Purpose
- issue 생성 시 필수 label 축이 모두 지정되었는지 검증.
- 허용되지 않은 `status`, `priority`, `area`, `source_type` 값을 차단.

## Trigger
- `scripts/repo/issue_create.sh` 실행 직전.

## Status
- `active`

## SoT
- [../issue-convention.md](../issue-convention.md)

## Enforcer
- [../../scripts/repo/issue_label_guard.py](../../scripts/repo/issue_label_guard.py)

## Dependencies
- [../issue-convention.md](../issue-convention.md)
- [../../scripts/repo/issue_create.sh](../../scripts/repo/issue_create.sh)

## Failure Mode
- 실패 시 issue 생성 차단.

## Tests
- [../../scripts/repo/tests/test_issue_label_guard.py](../../scripts/repo/tests/test_issue_label_guard.py)
