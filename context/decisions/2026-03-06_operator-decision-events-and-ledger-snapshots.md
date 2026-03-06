# DEC: Operator decision events and ledger snapshots for orchestration history

- Date: 2026-03-06
- Context: 수동 오케스트레이션 규격을 정리하는 과정에서 `packet`과 `trace`만으로는 operator의 판정 근거, 상태 전이, 재작업 사유를 충분히 복원하기 어렵다는 문제가 드러났다. 또한 `run ledger`를 최신 상태만 담는 projection으로 유지하면 운영은 편하지만, 특정 시점에 control-plane이 무엇을 보고 어떤 판정을 내렸는지의 audit trail이 약해진다. 자동 오케스트레이션으로 확장하려면 event ordering, operator decision, snapshot checkpoint가 모두 명시되어야 한다.
- Decision: orchestration artifact를 `packet`, `trace`, `operator decision`, `current run ledger`, `snapshot ledger`의 5계층으로 운영한다.
  - 모든 runtime artifact는 `run-local seq`를 가져 총순서를 만든다.
  - `packet`과 `trace`는 append-only 원본 이력으로 유지한다.
  - operator의 `accept/rework/block/cancel/remediate/close` 판정은 `trace`에 섞지 않고 별도 `operator decision event` artifact로 남긴다.
  - `current run ledger`는 각 `run_id`당 1개만 두고 최신 상태 projection의 SoT로 사용한다.
  - `snapshot ledger`는 operator decision 직후 append-only로 남겨, 그 시점의 control-plane 상태를 고정한다.
  - `trace`는 machine field와 narrative field를 분리하고, 테스트/스킵/리스크/블로커는 구조화된 객체로 기록한다.
- Alternatives: `trace`에 operator 판정을 같이 적는다. `run ledger` 하나만 최신 상태로 유지하고 과거 snapshot은 남기지 않는다. 파일명과 시간값만으로 정렬하고 별도 `seq`는 두지 않는다.
- Tradeoffs: artifact 종류와 관리 비용이 증가하고 validator/schema도 복잡해진다. 대신 operator 판단 근거, 재작업 원인, 상태 전이 이력이 분리되어 audit/replay/debugging이 쉬워진다. `current ledger`는 가볍게 유지하면서도 `snapshot ledger`로 과거 상태를 복원할 수 있다.
- Revisit if: runtime artifact 수가 지나치게 늘어 운영 비용이 커지거나, decision event 없이도 자동 라우터가 충분히 안정적으로 동작함이 입증될 때. 또는 snapshot checkpoint 빈도가 과도해 관리성이 떨어질 경우 snapshot 정책을 축소한다.
