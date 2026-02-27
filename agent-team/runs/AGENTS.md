# Layer 3 Maintenance / Run Policy

## 목적
- `agent-team/runs/` 범위에서 작업 이력 문서의 갱신 순서와 피드백 반영 정책을 정의한다.

## 필수 갱신 순서
1. `task-brief.json`
2. `trace.md`
3. `run-log.md` (span 실행 시마다 누적 기록)
4. 실행 산출물(예: `problem-definition.md`)
5. `run-report.json`
6. `feedback-record.json`(재작업/실패 시)
7. `status.md`

## span 기록 최소 항목
- `span_id`
- `owner_agent`
- `input_artifacts` / `output_artifacts`
- `acceptance_check_result`
- `human_decision`
- `next_span`

## 반영 조건
- 실패 1회: 로컬 수정 후 재시도
- 동일 실패 2회: `feedback-record.json`에 root cause와 process/codebase 개선안 필수 기록
- 동일 실패 3회(주간): `ops/weekly-batch-loop.md` 실험 안건으로 승격

## 만료 규칙
- 임시 운영 규칙은 상태 파일에 `expires_at` 또는 만료 조건을 기록한다.
- 만료 조건이 충족되면 유지보수 검토에서 삭제 후보로 이동한다.
