# Weekly Batch Optimization Loop

## Objective
Improve system-level performance by evaluating repeated failures and optimizing protocol/persona/process design.

## Cadence
- Weekly review window: one fixed review session.
- Data window: latest 7 days of `RunReport`, `FeedbackRecord`, `run-log.md` span 기록.

## Weekly Process
1. Aggregate metrics: accuracy, rework rate, token cost.
2. Inspect span-level bottlenecks from `run-log.md` (반복 반려 span, 잦은 회귀 경로).
3. Select top 3 recurring failure clusters.
4. For each cluster, draft 2 intervention candidates:
   - process/codebase intervention
   - routing/prompt intervention
5. Define A/B test with acceptance thresholds.
6. Run controlled trial on representative tasks.
7. Approve one of:
   - promote change,
   - iterate,
   - rollback.
8. Update protocol/persona docs only for promoted changes.

## Promotion Order
1. Process and codebase fixes
2. AGENTS routing/policy adjustments
3. Prompt/config tuning

## Promotion Criteria
- Accuracy improves without disproportionate cost increase.
- Rework rate decreases for targeted failure tags.
- No regression on safety/approval compliance.

## Rollback Triggers
- Accuracy decreases materially.
- Rework rate increases for unrelated categories.
- Human reviewers report reduced clarity or control.

## Meeting Artifacts
- Weekly KPI snapshot
- Span bottleneck report
- Failure cluster ranking
- Experiment log
- Change decision register
