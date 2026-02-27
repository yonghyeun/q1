# Online Feedback Loop (Per Task)

## Objective
Capture quality signals after every task and route immediate improvements.

## Workflow
1. Planner or Leader emits `TaskBrief`.
2. Leader(또는 Planner) writes `trace.md` with span map and gate rules.
3. Team executes one span at a time.
4. For every span, human records decision/evidence in `run-log.md`.
5. If span is accepted, move to next span; if not, follow retry/rollback path in `trace.md`.
6. At stage boundary, human performs ADLC gate approval.
7. Team records `RunReport`.
8. If failed or rework requested, create `FeedbackRecord` with `change_target`.
9. Leader decides next step: retry, redesign, or defer.

## Routing Rules
- Rework count `>= 2` for same tag: force root-cause review before retry.
- `risk_level=high`: reviewer + human gate mandatory before progression.
- Missing acceptance checks: bounce back to Planner.
- Missing run-log span entry: block progression until log is completed.

## Minimum Data to Log
- Task ID / span_id / ADLC stage
- Owner agent
- Input artifacts / output artifacts
- Acceptance check result (pass/fail + reason)
- Human decision
- Token cost
- Latency
- Rework count
- Failure tags

## Immediate Improvement Policy
- First failure: local fix and retry.
- Second same-category failure: root-cause + structural fix proposal(process/codebase 우선).
- Third same-category failure in week: escalate to weekly batch agenda.

## Update Queue Rule
- `FeedbackRecord.change_target=process|codebase`는 즉시 개선 큐에 등록한다.
- `change_target=prompt|agents_doc|config`는 주간 배치 승인 후 반영한다.
