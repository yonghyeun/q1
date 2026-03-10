# Gate: issue-body

## Purpose
- issue 본문이 type별 GitHub 템플릿 구조를 따르는지 검증.
- placeholder, 빈 섹션, 필수 섹션 누락을 차단.

## Trigger
- `scripts/repo/issue_create.sh` 실행 직전.

## Status
- `active`

## SoT
- [../issue-convention.md](../issue-convention.md)
- [../../.github/ISSUE_TEMPLATE/feature.md](../../.github/ISSUE_TEMPLATE/feature.md)
- [../../.github/ISSUE_TEMPLATE/bug.md](../../.github/ISSUE_TEMPLATE/bug.md)
- [../../.github/ISSUE_TEMPLATE/chore.md](../../.github/ISSUE_TEMPLATE/chore.md)

## Enforcer
- [../../scripts/repo/issue_body_quality_guard.py](../../scripts/repo/issue_body_quality_guard.py)

## Dependencies
- [../../scripts/repo/body_guard_common.py](../../scripts/repo/body_guard_common.py)
- [../../scripts/repo/issue_create.sh](../../scripts/repo/issue_create.sh)
- [../../.github/ISSUE_TEMPLATE/feature.md](../../.github/ISSUE_TEMPLATE/feature.md)
- [../../.github/ISSUE_TEMPLATE/bug.md](../../.github/ISSUE_TEMPLATE/bug.md)
- [../../.github/ISSUE_TEMPLATE/chore.md](../../.github/ISSUE_TEMPLATE/chore.md)

## Failure Mode
- 실패 시 issue 생성 차단.

## Tests
- [../../scripts/repo/tests/test_issue_body_quality_guard.py](../../scripts/repo/tests/test_issue_body_quality_guard.py)
