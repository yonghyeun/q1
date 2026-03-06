# Agent Handoff Schema

수동 오케스트레이션 기반 멀티 에이전트 개발에서 사용하는 handoff packet / work trace 표준을 정의한다.

목표는 3가지다.

1. 사람이 읽고 판단할 수 있어야 한다.
2. 이후 자동 오케스트레이션으로 승격할 수 있어야 한다.
3. 병렬 작업 중 context loss, contract drift, merge rework를 줄여야 한다.

## 기본 입장

- 기본 포맷은 **Markdown 문서 + 고정된 구조의 YAML block**을 권장한다.
- handoff는 **task packet**과 **trace summary**를 분리한다.
- operator 상태 전이는 `operator decision event`로 별도 관리한다.
- 원 요청은 자주 바꾸지 않고, 실행 결과는 append-only에 가깝게 남긴다.
- `packet`은 가능한 한 불변(immutable)으로 유지하고, runtime 상태는 `trace`와 `run ledger`가 책임진다.

이 구조는 아래의 표준적 운영 패턴을 섞어 가져온다.

- Issue/Ticket 시스템의 작업 명세
- API/contract-first 개발의 입력/출력 명세
- Shift handoff/runbook의 상태/리스크 요약
- CI artifact의 검증 결과 기록

## 왜 packet과 trace를 분리하나

`packet`은 "무엇을 해야 하는가"를 고정한다.
`trace`는 "실행 중 무슨 일이 있었는가"를 기록한다.

둘을 하나로 섞으면 아래 문제가 생긴다.

- 원래 목표가 실행 도중 덮어써진다.
- 다음 에이전트가 "현재 상태"와 "원래 요구"를 구분하지 못한다.
- 자동화 시 라우팅 기준과 이력 기준이 분리되지 않는다.

따라서 권장 원칙은 다음과 같다.

- `packet`: 상대적으로 안정적, 필요 시 새 packet으로 supersede
- `trace`: 실행 중 계속 누적
- `operator decision`: trace 검토 후 상태 전이 판단을 기록

## 식별과 정렬

runtime artifact는 모두 `run_id`와 `seq`를 가져야 한다.

- `run_id`: 어떤 orchestration run에 속하는지
- `seq`: run 내부 총순서를 만드는 정수

파일명은 탐색용이고, 실제 정렬/참조는 artifact 내부 `seq`와 ID를 기준으로 한다.

## 표준 운영 원칙

### 1. Link over copy

- 긴 문맥은 handoff에 복붙하지 않고 파일 경로로 참조한다.
- 핵심 요약만 packet에 넣고, 세부 계약은 원문 SoT를 링크한다.

### 2. Contract before implementation

- 병렬 작업에 들어가기 전 `contracts`, `acceptance criteria`, `owned paths`를 먼저 고정한다.
- 이 3개가 없으면 handoff-ready 상태로 보지 않는다.

### 3. Explicit ownership

- 각 handoff는 책임 에이전트와 파일/모듈 ownership을 명시한다.
- ownership이 겹치면 병렬성보다 통합 비용이 커지므로 재분할을 우선 검토한다.

### 4. Append-only trace

- trace는 이전 상태를 덮어쓰기보다, 결정/실패/검증 결과를 누적하는 방식이 좋다.
- 자동화 시 retry, escalation, audit 근거로 재사용할 수 있다.

### 5. Structured outputs

- 완료 보고는 자유 서술보다 `changes`, `tests`, `risks`, `next_action` 같은 고정 필드를 우선한다.
- 사람이 읽기 쉬우면서도 나중에 operator agent가 파싱하기 쉽다.

### 6. Mandatory evaluation and feedback

- handoff는 "작업 전달"만이 아니라 "평가 가능한 결과 반환"까지 포함해야 한다.
- 따라서 각 packet은 최소한의 pass/fail 기준과, 실패 시 어디에 피드백을 반영할지의 경로를 가져야 한다.
- 중요한 점은 실패가 곧바로 "담당 에이전트의 구현 실패"를 뜻하지는 않는다는 것이다.
- 실패는 `implementation`, `contract`, `wbs`, `harness`, `orchestration` 레이어 어디서든 발생할 수 있다.

## 권장 packet 스키마

아래는 최소 권장 필드다.

```yaml
packet_id: H-2026-03-06-001
run_id: RUN-2026-03-06-A
seq: 1
slice_id: MVP-TS-INSERT
parent_wbs: mvp-wbs/v1
owner_role: impl
handoff_from: operator
handoff_to: impl
supersedes_packet_id:
goal: 현재 재생 시점을 노트에 마크다운 타임스탬프로 삽입한다.
why: 타임스탬프 레퍼런싱은 핵심 학습 UX다.
inputs:
  - docs/product/mvp-spec.md:61
  - docs/product/contracts/domain.ts:29
  - docs/product/contracts/storage.ts:18
contracts:
  - docs/product/contracts/domain.ts
  - docs/product/contracts/storage.ts
acceptance_criteria:
  - 버튼 클릭 시 현재 시점이 markdown 링크로 삽입된다.
  - 삽입 후 외부 이동 없이 앱 내부 seek과 호환된다.
  - 자동저장과 충돌하지 않는다.
owned_paths:
  - apps/web/src/features/timestamp/**
non_goals:
  - 키보드 단축키 구현
  - 타임스탬프 클릭 seek 구현
dependencies:
  - player time adapter
  - note editor command surface
required_tests:
  - unit
  - integration
validator_rules:
  - inputs_resolve
  - contract_paths_resolve
  - owned_paths_declared
  - required_tests_declared
review_rubric:
  - acceptance_criteria_evidenced
  - no_contract_violation
  - no_owned_path_violation
  - next_actor_can_decide
escalation_policy:
  on_block: operator_review
  on_contract_break: contract_owner_review
  on_repeat_failure: revisit_wbs
expected_outputs:
  - code_changes
  - tests
  - trace_summary
open_risks:
  - player time source가 아직 fake adapter로만 존재할 수 있음
```

## packet 필드 설명

- `packet_id`: handoff 단위의 고유 ID
- `run_id`: 소속 orchestration run
- `seq`: run 내부 총순서
- `slice_id`: WBS 기준 작업 슬라이스 ID
- `parent_wbs`: 어떤 WBS 버전을 기준으로 생성된 packet인지
- `owner_role`: 현재 packet 책임 역할
- `supersedes_packet_id`: 이전 packet을 대체하는 재발행이면 참조
- `goal`: 한 문장으로 끝나는 목표
- `why`: 제품/운영 관점의 이유
- `inputs`: 읽어야 하는 최소 입력
- `contracts`: 구현 전 반드시 맞춰야 하는 접점 SoT
- `acceptance_criteria`: 완료 판정 기준
- `owned_paths`: 수정 책임이 있는 파일 경계
- `non_goals`: 이번 handoff에서 하지 않을 것
- `dependencies`: 선행 의존성
- `required_tests`: 최소 테스트 레벨
- `validator_rules`: 기계가 검증할 수 있는 최소 규칙
- `review_rubric`: operator가 증거를 보고 판단해야 하는 평가 기준
- `escalation_policy`: 실패 유형별 기본 escalation 경로
- `expected_outputs`: 결과물 형식
- `open_risks`: 시작 시점에 이미 알려진 위험

## 권장 trace summary 스키마

trace는 packet과 별도 문서 또는 별도 섹션으로 관리한다.

```yaml
trace_id: T-2026-03-06-014
run_id: RUN-2026-03-06-A
seq: 2
packet_id: H-2026-03-06-001
slice_id: MVP-TS-INSERT
agent_role: impl
attempt_index: 1
execution_state: review_required
result: partial
failure_type: orchestration
started_at: 2026-03-06T10:00:00+09:00
ended_at: 2026-03-06T10:24:00+09:00
summary: editor insert command 계약 부재로 integration-ready 판정이 불가했다.
artifacts_used:
  - docs/product/mvp-spec.md:61
changes:
  - apps/web/src/features/timestamp/insert-timestamp.ts
  - apps/web/src/features/timestamp/insert-timestamp.test.ts
tests_run:
  - command: pnpm test -- timestamp
    result: passed
tests_skipped:
  - command: pnpm test -- timestamp-integration
    reason_code: missing_input
    reason_detail: editor command surface 계약이 packet inputs에 없다.
decisions_made:
  - timestamp format은 HH:MM:SS를 고정
new_facts:
  - 현재 packet만으로는 note editor insert command의 입력/출력 경계가 복원되지 않는다.
blockers: []
risks:
  - code: editor_surface_undefined
    detail: editor adapter가 바뀌면 command surface 수정이 필요하다.
feedback:
  - target: harness
    severity: should_fix
    note: fake player adapter의 시간이 불안정해 integration assertion이 흔들릴 수 있음
  - target: packet
    severity: must_fix
    note: editor command surface 명세가 inputs에 더 명확히 적혀야 함
requested_decision: rework
next_action: integration agent가 editor wiring을 검토
decision_rationale: 입력 부족이 원인이므로 구현 재시도보다 packet 보강 후 재작업이 적절하다.
context_notes:
  - 이번 handoff는 markdown 생성 로직까지는 검증했지만 editor wiring은 닫지 못했다.
confidence: medium
```

## trace 필드 설명

- `run_id`: 소속 orchestration run
- `seq`: run 내부 총순서
- `execution_state`: 현재 실행 상태 (`in_progress | blocked | review_required | done`)
- `attempt_index`: 같은 packet 아래 몇 번째 시도인지
- `result`: 이번 실행의 자기 평가 결과 (`success | partial | failed`)
- `failure_type`: 주요 실패 원인 분류 (`none | implementation | contract | missing_input | harness | orchestration | wbs`)
- `summary`: 이번 실행의 짧은 상태 요약
- `artifacts_used`: 실제 읽은 입력/증거 참조
- `changes`: 실제 수정 파일
- `tests_run`: 실행한 검증 명령과 결과
- `tests_skipped`: 건너뛴 검증 명령과 이유 코드/상세
- `decisions_made`: 구현 중 새로 생긴 결정
- `new_facts`: 이번 실행으로 새로 드러난 사실
- `blockers`: 즉시 해결이 필요한 장애 코드와 상세
- `risks`: 아직 남아 있는 리스크 코드와 상세
- `feedback`: packet/WBS/contract/harness/orchestration에 반영해야 할 피드백
- `requested_decision`: trace 작성자가 operator에게 권장하는 다음 판정
- `next_action`: 다음 담당자에게 기대하는 한 줄 액션
- `decision_rationale`: 왜 그 판정을 권장하는지에 대한 서술
- `context_notes`: 다음 actor/operator가 알아야 할 서술형 맥락
- `confidence`: `low | medium | high`

## 상태 소유권

현재 상태는 아티팩트별로 분리해서 관리하는 것을 권장한다.

- `packet`: handoff 명세 자체를 담고, runtime 상태는 갖지 않는다
- `trace.execution_state`: 개별 실행의 현재 상태를 나타낸다
- `operator decision`: trace 검토 후 내려진 상태 전이 판단을 남긴다
- `run ledger`: 현재 slice 상태, active packet, next decision의 SoT를 가진다

## 평가 기준과 실패 분류

handoff 결과는 `validator_rules`와 `review_rubric`을 나눠서 평가하는 것을 권장한다.

### 1. Validator rules

기계가 판정 가능한 조건이다.

- 참조 경로가 존재하는가
- `owned_paths`가 선언되어 있는가
- `required_tests`가 선언되어 있는가
- 필수 필드가 누락되지 않았는가

### 2. Review rubric

사람이 trace와 증거를 보고 판단해야 하는 조건이다.

1. 목표가 handoff 범위 안에서 실질적으로 진전됐는가
2. acceptance criteria에 대한 증거가 남아 있는가
3. required tests가 통과했거나, 미실행 사유가 명시됐는가
4. contracts와 owned paths를 위반하지 않았는가
5. 다음 actor가 판단 가능한 수준의 trace를 남겼는가

실패는 아래처럼 분류하는 것을 권장한다.

- `implementation failure`: 구현이 미완성/오작동
- `contract failure`: 인터페이스나 데이터 형식이 SoT와 불일치
- `missing_input failure`: 입력 정보/의존성이 부족해 진행 불가
- `harness failure`: 테스트 하네스나 fake/integration 환경이 신뢰 불가
- `orchestration failure`: handoff packet, ownership, routing이 부정확
- `wbs failure`: slice 경계나 AC 자체가 잘못 정의됨

중요한 원칙은, 실패를 "누가 못했는가"보다 "어느 레이어를 수정해야 하는가"로 분류하는 것이다.

## 피드백 루프

trace의 피드백은 최소한 아래 5개 대상으로 되돌아갈 수 있어야 한다.

- `packet`: 이번 handoff 설명이 부족했는지 수정
- `wbs`: slice 분해나 AC 정의를 수정
- `contracts`: 인터페이스 SoT를 정정/승격
- `harness`: 검증 환경, fixture, fake adapter를 수정
- `orchestration`: 상태 모델, routing 규칙, operator 절차를 수정

권장 원칙은 다음과 같다.

- 동일 유형 실패가 2회 이상 반복되면 packet rework로만 끝내지 말고 상위 문서에 피드백을 반영한다.
- `harness`나 `orchestration` 피드백은 구현 에이전트의 책임으로 덮지 않는다.
- `wbs` 실패가 의심되면 진행 중인 하위 packet을 더 늘리기보다 slice 재설계를 우선 검토한다.

## 상태 전이 권장안

표준적으로는 실행 상태 수를 적게 유지하는 것이 좋다.

- `trace.execution_state`
  - `in_progress`: 현재 수행 중
  - `blocked`: 외부 입력/결정이 필요함
  - `review_required`: 구현은 끝났고 검토/통합 필요
  - `done`: 실행 종료

`paused`, `waiting`, `retrying` 같은 세분화 상태는 초기에 넣지 않는 것을 권장한다.
상태가 많아질수록 오퍼레이터와 자동 라우터가 모두 불안정해진다.

## 표준적 대안과 trade-off

### A. 자유 서술형 handoff

- 장점: 빠르게 시작 가능
- 단점: 품질 편차가 크고 자동화가 거의 불가능

### B. 체크리스트형 ticket

- 장점: 운영이 단순하고 누락 방지에 좋음
- 단점: 작업 trace와 맥락 전달이 얕아 복잡한 통합에 약함

### C. DAG/workflow engine 선도입

- 장점: 장기적으로 자동화 잠재력이 큼
- 단점: 초기 routing rule과 retry model이 불안정하면 오히려 실패를 확대

### D. Packet + Trace 분리형 하이브리드

- 장점: manual-first와 gradual automation 사이의 균형이 좋음
- 단점: 문서 2개 레이어를 관리해야 하므로 discipline이 필요

현재 단계에서는 **D안**을 기본 추천으로 둔다.

## 자동화 전환 조건

아래가 반복적으로 만족될 때만 operator 역할의 일부를 자동화 후보로 본다.

- packet 필드 누락률이 낮다.
- trace summary 형식이 안정적으로 반복된다.
- handoff failure 원인이 schema 부재가 아니라 예외 케이스로 수렴한다.
- 동일한 routing 판단이 여러 번 반복된다.

자동화 우선순위는 아래 순서를 권장한다.

1. packet validator
2. trace summarizer
3. readiness checker
4. low-risk routing assistant
5. full operator automation

## 이 저장소 기준 권장안

- handoff packet은 `context/wbs/` 아래 문서로 관리한다.
- 제품/계약 SoT는 `docs/`와 `context/core/`를 참조하고 복제하지 않는다.
- 각 vertical slice는 최소한 `goal`, `contracts`, `acceptance_criteria`, `owned_paths`, `required_tests`가 채워진 뒤에만 병렬로 분기한다.
- 자동 오케스트레이션은 지금 당장 기본값으로 두지 않고, 수동 운영에서 검증된 반복 패턴만 승격한다.
