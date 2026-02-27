# Runs Directory Guide (Task-ID 중심)

## 폴더 구조
- 작업 단위 폴더: `agent-team/runs/T-000N/`
- ID 레지스트리: `agent-team/runs/index.json`

## 필수 파일
- `task-brief.json`
- `trace.md`
- `run-log.md`
- `run-report.json` (task 종료/판정 시 필수)
- `status.md`

## 선택 파일
- `leader-plan.json` (복잡한 task에서 권장)
- `handoff.json` (특정 역할/수용 기준 강화 시 권장)
- `feedback-record.json` (재작업/실패 시 권장)
- 단계 산출물 파일(예: `problem-definition.md`)

## 업데이트 순서
1. `task-brief.json`
2. `trace.md` (span map + gate + 평가 기준)
3. span 실행 + `run-log.md` 기록
4. 실행 산출물(예: `problem-definition.md`)
5. `run-report.json`
6. `feedback-record.json` (필요 시)
7. `status.md`

## 커밋 매핑
- Explore: `task-brief.json` 중심
- Design: `trace.md` 중심 (필요 시 `leader-plan.json`/`handoff.json` 포함)
- Execute: 산출물 + `run-log.md` + `run-report.json`
- Improve: `feedback-record.json` + `status.md`
