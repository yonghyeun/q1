# Task 단위 커밋 정책

## 원칙
- 한 커밋은 하나의 `task-id`와 하나의 ADLC 단계만 다룬다.
- 커밋 메시지는 저장소 `commit-msg` hook 규칙을 따른다.
- 커밋 전 `agent-team/runs/<task-id>/status.md`를 현재 단계로 갱신한다.
- 커밋 메시지는 `ops/templates/commit-message.template.txt`를 기준으로 작성한다.
- SoT 관련 변경(`agent-team/sot`, `agent-team/subagents`)에는 생성된 `.codex/` 결과를 함께 커밋한다.

## 권장 커밋 순서
1. `explore`: `task-brief.json`, 초기 상태 문서
2. `design`: `leader-plan.json`, handoff 설계
3. `execute`: 산출물 + `run-report.json`
4. `improve`: `feedback-record.json`, 개선 조치

## 메시지 예시
- `docs(doc) : T-0002 탐색 결과 문서 정리`
- `config(infra) : T-0002 커밋 훅 검증 규칙 적용`
