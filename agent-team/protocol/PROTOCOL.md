# ADLC Protocol v0.1.0

## Purpose
This protocol routes work across the Core 4 agent team for SaaS exploration/ideation.
It contains only non-discoverable operating rules: role routing, approval gates, KPIs, and safety constraints.

## Lifecycle
Use the ADLC lifecycle for every task:
1. Explore
2. Design
3. Execute
4. Improve

## Execution Model (v0.1.0)
- `task-brief.json`까지는 사용자 의도와 범위를 확정하는 입력 단계다.
- `task-brief.json` 이후는 `trace.md`를 기준으로 수동 span 실행을 수행한다.
- 각 span은 사람이 직접 판정하며(`approved|changes_requested|rejected`), 판정 근거는 `run-log.md`에 기록한다.
- 단계 게이트(Explore/Design/Execute/Improve)는 기존 정책대로 human approval required를 유지한다.

## Roles
- `adlc-leader`: Owns goal alignment, decomposition, routing, and final gate orchestration.
- `planner-pm`: Converts goals into hypotheses, experiments, and acceptance criteria.
- `builder`: Produces artifacts and implementation options.
- `reviewer`: Validates quality, risks, counterexamples, and rework requests.

## Routing Rules
- If a request is ambiguous, route first to `planner-pm`.
- If a request is implementation-heavy, route to `builder` with explicit acceptance checks.
- If a request has material risk, novelty, or user-facing impact, add `reviewer` before approval.
- `adlc-leader` must provide final synthesis and gate decisions.

## Human-in-the-Loop Gate (Initial Policy)
All major ADLC stages require human approval:
- Explore output approval
- Design plan approval
- Execute result approval
- Improve action approval

Do not auto-skip gates. Suggest gate relaxation only in improvement reviews backed by evidence.

## Span-level Manual Operation Rule
- v0.1.0에서는 모든 span/node를 수동으로 진행한다.
- 다음 span으로 이동하기 전에 반드시 `run-log.md`에 아래를 남긴다:
  - span_id, owner_agent, input/output artifacts
  - acceptance check 판정(pass/fail) + 근거
  - human decision(approved/changes_requested/rejected)
  - next_span(재시도/회귀 포함)
- `run-log.md` 필수 항목 누락 시 다음 span 진행을 금지한다.

## Output Contract (Required Sections)
Every role output must include:
- `Plan`
- `Assumptions`
- `Risks`
- `Approval Needed`
- `Next Action`

## Decision Policy
- Optimize for quality and correctness first.
- Track cost and latency as ROI signals, not hard constraints.
- When uncertainty is high, shrink scope to hypothesis-driven experiments.
- Always present at least 2 viable options for major decisions with tradeoffs.

## Context Policy
- Do not include repository-discoverable information in protocol or persona files.
- Load context dynamically by task type; avoid broad static context.
- Prefer concise, high-signal context from the last 3 relevant failures.
- For branch/PR operations, follow `context/core/policy-routing.md` and enforce `policies/branch-policy.rules.json`.

## Failure Policy
- If the same failure class repeats twice:
  1. Perform root-cause classification.
  2. Prioritize process/codebase fixes.
  3. Modify prompt text only if structural fixes are insufficient.

## KPI Set
Track these primary metrics on every run:
- Accuracy (human approval pass rate)
- Rework rate (average retries per task)
- Token cost (tokens per completed task)
- Latency (seconds per span and per task)

## Artifacts
Use the interface contracts in `agent-team/interfaces/`:
- `task-brief.schema.json`
- `leader-plan.schema.json`
- `handoff-packet.schema.json`
- `run-report.schema.json`
- `feedback-record.schema.json`

Use operational markdown artifacts in `agent-team/runs/T-000N/`:
- `trace.md` (natural-language execution trace definition)
- `run-log.md` (span-by-span manual execution ledger)
