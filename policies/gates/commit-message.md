# Gate: commit-message

## Purpose
- 커밋 메시지가 저장소 형식을 따르는지 검증.
- 제목/설명 2줄 구조, category, layer, 한글 포함 규칙을 강제.

## Trigger
- local `commit-msg`.

## Status
- `active`

## SoT
- [../commit-convention.md](../commit-convention.md)

## Enforcer
- [../../.githooks/commit-msg](../../.githooks/commit-msg)

## Dependencies
- [../../.githooks/commit-msg](../../.githooks/commit-msg)
- [../commit-convention.md](../commit-convention.md)

## Failure Mode
- 실패 시 commit 차단.

## Tests
- 현재 전용 테스트 파일 없음.
