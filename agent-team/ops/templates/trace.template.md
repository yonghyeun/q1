# T-000N Trace (v0.1.0)

## 0) Task Meta
- Task ID: `T-000N`
- Title: <task title>
- Goal: <one sentence>
- Scope In: <key in-scope items>
- Scope Out: <key out-of-scope items>
- Deadline: <YYYY-MM-DD>
- Risk Level: <low|medium|high>

## 1) Definition of Done
- <완료 조건 1>
- <완료 조건 2>
- <완료 조건 3>

## 2) Span Map
| Span ID | Stage | Owner Agent | Objective | Inputs | Outputs | Acceptance Checks | On Fail |
|---|---|---|---|---|---|---|---|
| S1.explore.normalize | explore | planner-pm | Task 정의를 실행 가능한 문제로 정규화 | task-brief.json | explore-summary.md | 범위/제약/위험이 명시됨 | S1.explore.normalize 재시도 |
| S2.design.plan | design | adlc-leader | 실행 추적 계획 수립 | task-brief.json, explore-summary.md | leader-plan.json (optional) | 단계별 기준/게이트 명시 | S1 또는 S2로 회귀 |
| S3.execute.draft | execute | builder | 핵심 산출물 초안 작성 | task-brief.json, leader-plan.json(optional), handoff(optional) | artifact.md | 수용 기준 충족 | S3.execute.draft 재시도 |
| S4.execute.review | execute | reviewer | 산출물 검증 및 판정 | artifact.md | run-report.json | pass/fail 근거 명확 | S3로 회귀 |
| S5.improve.learn | improve | reviewer/adlc-leader | 실패 원인/개선안 구조화 | run-report.json | feedback-record.json(optional), status.md | 재발 방지안 명시 | S5.improve.learn 재시도 |

## 3) Gate Rules (Human Required)
- Explore Gate:
  - Approved -> Design stage 진입
  - Changes Requested -> S1 재실행
  - Rejected -> task-brief 재작성
- Design Gate:
  - Approved -> Execute stage 진입
  - Changes Requested -> S2 재실행
  - Rejected -> S1 또는 task-brief 재작성
- Execute Gate:
  - Approved -> Improve stage 진입
  - Changes Requested -> S3 재실행
  - Rejected -> S2 또는 S3 회귀
- Improve Gate:
  - Approved -> task completed
  - Changes Requested -> S5 재실행
  - Rejected -> 재계획 후 재시작

## 4) Logging Rule (Every Span)
각 span 종료 후 `run-log.md`에 반드시 기록:
- span_id / stage / owner_agent
- started_at / ended_at
- input_artifacts / output_artifacts
- acceptance_check_result(pass/fail + 근거)
- human_decision(approved/changes_requested/rejected)
- token_cost / latency (가능한 범위)
- risk_note
- next_span

## 5) Evaluation Rubric
- Quality: 요구 산출물 형식과 내용 충족 여부
- Measurability: 성공/실패 기준의 측정 가능성
- Risk: 누락된 리스크/범위 폭주 위험
- Reusability: 다음 유사 task에서 재사용 가능한지

## 6) Notes
- `leader-plan.json`, `handoff.json`은 필요 시 오버레이로 사용한다.
- 자동 실행 대신 수동 trace를 우선하며, run-log 누락 시 진행하지 않는다.
