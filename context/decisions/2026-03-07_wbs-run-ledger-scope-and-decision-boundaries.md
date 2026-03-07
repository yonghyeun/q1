# DEC: Run ledger scope and accept/dispatch decision boundaries

- Date: 2026-03-07
- Context: `context/wbs/open-questions.md`에 두 가지 미해결 항목이 남아 있었다. 첫째, `run ledger.slice_entries`가 runtime artifact가 이미 발행된 slice만 담을지, 아니면 WBS backlog 단계의 `planned`/`ready` slice까지 담을지가 정해지지 않았다. 둘째, packet 종료 승인(`accept`)과 다음 actor packet 발행(`dispatch`)을 항상 분리된 decision/event로 남길지, operator가 한 번에 처리해도 되는지가 열려 있었다. 이 상태로는 `run-ledger` schema의 필수 runtime 참조 필드, validator 의미, audit trail 경계가 모두 애매해질 수 있었다.
- Decision: `run ledger`는 runtime control-plane으로 한정하고, `accept`와 `dispatch`는 항상 분리된 operator decision/event로 기록한다.
  - `run ledger.slice_entries`는 runtime artifact가 이미 발행된 slice만 포함한다.
  - ledger entry는 첫 packet 발행 또는 그와 동치인 첫 dispatch 시점부터 생성한다.
  - `planned`/`ready` backlog는 WBS가 SoT로 유지하고, backlog overview가 필요하면 별도 projection/view로 해결한다.
  - `accept`는 현재 packet의 목적 충족과 종료 승인을 기록하는 event다.
  - `dispatch`는 다음 actor용 packet 발행을 기록하는 event이며 `next_packet_id`를 이 event가 소유한다.
  - operator가 UX 상으로 한 번에 처리하더라도 artifact는 `accept` seq N, `dispatch` seq N+1로 분리한다.
  - `accept`는 snapshot checkpoint 대상이고, `dispatch`는 기본적으로 current ledger만 갱신한다.
- Alternatives: run ledger에 `planned`/`ready` slice까지 포함해 backlog와 runtime을 한 화면에서 같이 본다. `accept`와 `dispatch`를 하나의 decision/event로 합쳐 운영 event 수를 줄인다.
- Tradeoffs: backlog와 runtime을 하나의 ledger로 합치는 편의는 포기한다. 또한 `accept`와 `dispatch`를 분리하면 event 수가 늘고 operator 구현도 조금 더 엄격해진다. 대신 `run ledger`는 runtime state projection이라는 역할이 분명해지고, validator와 schema가 단순해진다. 또 "왜 닫았는가"와 "왜 넘겼는가"의 사유가 분리되어 audit/replay/debugging이 쉬워진다.
- Revisit if: run ledger를 읽는 자동화 계층이 backlog와 runtime을 반드시 하나의 projection으로 요구하게 되거나, accept 직후 dispatch를 거의 항상 원자적으로 처리하는 실행기가 도입되어 분리 event의 비용이 이득보다 커질 때.
