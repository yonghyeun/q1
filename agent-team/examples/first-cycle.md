# Example: First ADLC Cycle

> v0.1.0 기준: `task-brief` 이후는 `trace.md`를 따라 span 단위 수동 실행 + `run-log.md` 기록.

## 1) Explore
- Input: `task-brief.template.json`
- Owner: `planner-pm`
- Output: refined problem statement + interview hypothesis
- Log: `run-log.md`에 S1 결과/근거 기록
- Gate: human approval required

## 2) Design
- Input: approved explore output
- Owner: `adlc-leader` (필요 시 `planner-pm` 보조)
- Output: `trace.md` + optional `leader-plan.template.json`
- Log: `run-log.md`에 S2 결과/근거 기록
- Gate: human approval required

## 3) Execute
- Input: approved trace plan + optional handoff
- Owner: `builder` (draft), `reviewer` (validation)
- Output: draft artifact + `run-report.template.json`
- Review: `reviewer` validates against acceptance checks
- Log: `run-log.md`에 span별 pass/fail + human decision 기록
- Gate: human approval required

## 4) Improve
- Input: `run-report.template.json` + optional `feedback-record.template.json`
- Owner: `adlc-leader` + `context-maintainer`
- Output: retry plan or weekly batch candidate
- Log: `run-log.md` 최종 요약과 `status.md` 동기화
- Gate: human approval required
