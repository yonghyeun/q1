# ADLC Protocol v1

## Purpose
This protocol routes work across the Core 4 agent team for SaaS exploration/ideation.
It contains only non-discoverable operating rules: role routing, approval gates, KPIs, and safety constraints.

## Lifecycle
Use the ADLC lifecycle for every task:
1. Explore
2. Design
3. Execute
4. Improve

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

## Artifacts
Use the interface contracts in `agent-team/interfaces/`:
- `task-brief.schema.json`
- `leader-plan.schema.json`
- `handoff-packet.schema.json`
- `run-report.schema.json`
- `feedback-record.schema.json`
