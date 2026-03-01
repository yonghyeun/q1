# Branch & PR Convention

## 브랜치
- 기본: `main`
- 작업 브랜치: `task/<task-id>-<short-topic>`
  - 예: `task/T-0007-adlc-gate-check`

## PR 원칙
- PR 설명에 작업 목적/범위/비범위 명시
- ADLC 산출물 링크 포함
- 리뷰어가 재현 가능한 검증 절차 포함

## 강결합 체크
머지 전 아래 산출물을 확인한다.
- `task-brief.json`
- `trace.md`
- `run-log.md`
- `run-report.json`
- 필요 시 `feedback-record.json`
