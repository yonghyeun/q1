# Run Artifact Conventions

이 문서는 orchestration run 내부 artifact의 파일 구조, 정렬 규칙, lineage 규칙을 정의한다.

## 목적

- `packet`, `trace`, `operator decision`, `run ledger`의 저장 위치를 통일한다.
- 파일명만으로도 대략적 흐름을 읽을 수 있게 한다.
- 실제 정렬과 참조는 파일명 관례가 아니라 artifact 내부 식별자/`seq`에 의존하도록 만든다.

## 기본 원칙

- 파일명은 탐색 편의용이다. **정본 식별자는 JSON 내부 필드**다.
- 모든 runtime artifact는 `run_id`와 `seq`를 가진다.
- 같은 run 안에서는 `seq`가 총순서를 만든다.
- `packet`과 `trace`는 수정하지 않고 새 artifact를 추가한다.
- `current run ledger`만 예외적으로 같은 경로를 갱신한다.

## 권장 디렉터리 구조

```text
context/wbs/examples/runs/<run_id>/
  current.run-ledger.json
  packets/
    0001.packet.<slice_id>.<actor>.json
  traces/
    0002.trace.<packet_id>.<actor>.json
  decisions/
    0003.decision.<slice_id>.<decision>.json
  snapshots/
    0003.<decision>.run-ledger.json
```

실제 운영 artifact도 이 구조를 기본값으로 삼는 것을 권장한다.

## 파일명 규칙

### Packet

`<seq>.packet.<slice_id>.<handoff_to>.json`

- 예: `0001.packet.MVP-TS-INSERT.impl.json`

### Trace

`<seq>.trace.<packet_id>.<agent_role>.json`

- 예: `0002.trace.H-2026-03-06-001.impl.json`

### Operator decision

`<seq>.decision.<slice_id>.<decision>.json`

- 예: `0003.decision.MVP-TS-INSERT.rework.json`

### Snapshot ledger

`<seq>.<decision>.run-ledger.json`

- 예: `0003.rework.run-ledger.json`

### Current ledger

`current.run-ledger.json`

## `seq` 규칙

- `seq`는 run 내부 단조 증가 정수다.
- packet, trace, decision, snapshot이 같은 카운터를 공유한다.
- 실제 정렬은 파일명보다 artifact 내부 `seq`를 기준으로 판정한다.
- timestamp는 참고 정보고, event ordering의 정본이 아니다.

## Lineage 규칙

### Packet lineage

- 재작업은 기존 packet 수정이 아니라 **새 packet 발행**이다.
- 새 packet은 `supersedes_packet_id`로 이전 packet과 연결한다.
- `run ledger.packet_history`는 packet disposition과 trace 요약을 함께 가진다.

### Trace lineage

- trace는 항상 정확히 하나의 `packet_id`를 가리킨다.
- 같은 packet에 여러 trace가 생길 수 있다.
- `attempt_index`는 같은 packet 아래에서만 증가한다.

### Decision lineage

- operator decision은 reviewed trace 집합을 기준으로 만들어진다.
- snapshot ledger는 해당 `decision_id`를 가리켜야 한다.
- `accept`와 `dispatch`를 함께 처리하더라도 하나의 decision으로 합치지 않고, 연속된 `seq`를 가진 두 artifact로 남긴다.

## Current vs Snapshot

### Current ledger

- 최신 상태 projection
- 각 `run_id`당 1개
- operator와 자동화가 기본적으로 읽는 문서
- `current_packet_id`는 slice 기준 최신 packet이며, 반드시 `active` 상태 packet만 뜻하지는 않는다.

### Snapshot ledger

- 특정 decision 시점의 frozen projection
- append-only
- 사후 분석, replay, audit 근거

## Snapshot 체크포인트

snapshot ledger는 최소한 아래 시점에 남기는 것을 권장한다.

- operator가 `rework`를 결정한 직후
- operator가 `block` 또는 `cancel`을 결정한 직후
- operator가 `accept` 또는 `close`를 결정한 직후
- remediation packet을 발행하는 decision 직후
- `dispatch`는 기본적으로 current ledger만 갱신하고 snapshot은 생략한다.

## Trade-offs

### 장점

- 파일 탐색과 event replay가 쉬워진다
- operator 판단과 actor 실행을 분리해 디버깅이 좋아진다
- 최신 상태와 과거 상태를 동시에 관리할 수 있다

### 단점

- artifact 수가 늘어난다
- `seq` 발급 discipline이 없으면 ordering이 무너진다
- current ledger와 snapshot ledger를 함께 관리해야 한다
