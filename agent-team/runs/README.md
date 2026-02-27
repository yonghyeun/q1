# Runs Directory Guide (Task-ID 중심)

## 폴더 구조
- 작업 단위 폴더: `agent-team/runs/T-000N/`
- ID 레지스트리: `agent-team/runs/index.json`

## 필수 파일
- `task-brief.json`
- `leader-plan.json`
- `handoff.json`
- `run-report.json`
- `status.md`

## 선택 파일
- `feedback-record.json` (재작업/실패 시 권장)
- 단계 산출물 파일(예: `problem-definition.md`)

## 업데이트 순서
1. `task-brief.json`
2. `leader-plan.json`
3. `handoff.json`
4. 실행 산출물
5. `run-report.json`
6. `feedback-record.json` (필요 시)
7. `status.md`

## 커밋 매핑
- Explore: `task-brief.json` 중심
- Design: `leader-plan.json` 중심
- Execute: 산출물 + `run-report.json`
- Improve: `feedback-record.json` + `status.md`
