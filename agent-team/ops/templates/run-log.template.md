# T-000N Run Log (v0.1.0)

- Task ID: `T-000N`
- Trace File: `trace.md`
- Operator: <human name or id>
- Started At: <ISO-8601>
- Current Stage: <explore|design|execute|improve>
- Current Status: <in_progress|blocked|completed>

---

## Span Entry Template
### [Span] <span_id>
- Stage: <explore|design|execute|improve>
- Owner Agent: <adlc-leader|planner-pm|builder|reviewer|subagent>
- Started At: <ISO-8601>
- Ended At: <ISO-8601>
- Input Artifacts:
  - <path>
- Output Artifacts:
  - <path>
- Acceptance Check Result:
  - <pass|fail>
  - Evidence: <why>
- Human Decision:
  - <approved|changes_requested|rejected>
  - Decision Note: <why>
- Cost & Latency:
  - token_cost: <int or n/a>
  - latency_seconds: <float or n/a>
- Risk Note:
  - <identified risk or none>
- Next Span:
  - <next span id or retry span id>

---

## Running Summary
- Total Spans Executed: <number>
- Approved Count: <number>
- Changes Requested Count: <number>
- Rejected Count: <number>
- Rework Count: <number>
- Open Risks:
  - <risk list>

## Finalization Checklist
- [ ] Every executed span has a log entry.
- [ ] Every span decision has explicit rationale.
- [ ] Run summary numbers match `run-report.json`.
- [ ] If failure/rework exists, `feedback-record.json` is created or planned.
