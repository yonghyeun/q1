# T-0001 Trace (v0.1.0)

## 0) Task Meta
- Task ID: `T-0001`
- Title: 브랜치 거버넌스 정책/검증 체계 구축
- Goal: 브랜치 규칙을 문서 + 자동 검증으로 강제한다.
- Scope In: 정책 SoT, 훅, CI, 정책 라우팅 문서
- Scope Out: 원격 저장소 관리자 설정 자동화
- Deadline: 2026-03-08
- Risk Level: medium

## 1) Definition of Done
- `task/i<issue>-T-000N-...` 네이밍 검증이 훅/CI에서 동일하게 동작한다.
- `main` 직접 작업이 로컬 훅에서 차단된다.
- PR 필수 산출물 검증(`task-brief.json`, `trace.md`, `run-log.md`, `run-report.json`)이 CI에서 차단된다.
- PR 본문의 `Closes #<issue>`가 브랜치 issue 번호와 일치해야 CI를 통과한다.
- feature/bug/chore issue 템플릿과 PR 템플릿이 저장소에 배치된다.
- 에이전트는 `context/core/policy-routing.md` 기반으로 정책 문서를 최소 로드한다.

## 2) Span Map
| Span ID | Stage | Owner Agent | Objective | Inputs | Outputs | Acceptance Checks | On Fail |
|---|---|---|---|---|---|---|---|
| S1.explore.policy | explore | planner-pm | 브랜치 컨벤션 요구사항/강제수단 정리 | 사용자 요청, 기존 policies | task-brief.json | 규칙과 강제 지점이 명확함 | S1 재시도 |
| S2.design.arch | design | adlc-leader | 문서/검증/라우팅 아키텍처 설계 | task-brief.json | trace.md, architecture doc | SoT 단일화 및 토큰 전략 합의 | S1 회귀 |
| S3.execute.impl | execute | builder | 훅/스크립트/CI/문서 구현 | trace.md | 코드/문서 변경 | validate-name/context/pr 동작 | S2 회귀 |
| S4.execute.verify | execute | reviewer | 단위/E2E 검증 및 리스크 평가 | 구현 결과 | run-log.md, run-report.json | 테스트 통과/예상 실패 케이스 확인 | S3 재시도 |
| S5.improve.wrapup | improve | adlc-leader | 운영 반영 및 후속과제 정리 | run-report.json | status.md | 다음 실행 액션 명확 | S4 회귀 |
| S6.improve.issue-transition | improve | adlc-leader | issue-driven 전략 전환 반영 | policy/docs/scripts | workflow + templates + cleanup script | issue 추적/정리 규칙 일관성 | S5 회귀 |

## 3) Gate Rules (Human Required)
- Explore Gate: approved
- Design Gate: approved
- Execute Gate: approved
- Improve Gate: approved

## 4) Logging Rule (Every Span)
각 span 종료 후 `run-log.md`에 span_id, 결과, human decision을 기록한다.

## 5) Evaluation Rubric
- Quality: 정책과 구현의 불일치 여부
- Measurability: 훅/CI에서 pass/fail 재현 가능 여부
- Risk: 우회/오검출 가능성
- Reusability: 이후 task에도 재사용 가능한 검증 엔진 여부

## 6) Notes
- 검증 엔진은 `scripts/repo/branch_guard.py`로 단일화한다.
