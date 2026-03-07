# WBS Open Questions

현재 WBS 운영 문서는 정합성을 맞췄지만, 아래 항목은 실제 `mvp-wbs.md`를 쓰기 전에 합의가 필요하다.

## 1. Run ledger가 어떤 slice까지 포함할 것인가

- 질문: `run ledger.slice_entries`는 이미 runtime artifact가 발행된 slice만 포함하는가, 아니면 packet 발행 전 `planned`/`ready` slice도 포함하는가.
- 현재 가정: 현 schema는 `current_packet_id`, `latest_trace_id`, `latest_decision_id`를 필수로 두므로 **runtime에 진입한 slice 중심**으로 설계돼 있다.
- trade-off:
  - runtime 진입 slice만 담으면 schema와 validator가 단순해진다.
  - `planned`/`ready` slice까지 담으면 operator가 backlog와 active work를 한 화면에서 볼 수 있지만, packet/trace/decision 참조를 optional로 풀어야 한다.

## 2. `accept`와 `dispatch`를 항상 분리할 것인가

- 질문: 현재 packet 종료 승인(`accept`)과 다음 actor packet 발행(`dispatch`)을 항상 별도 decision/event로 남길지, operator가 한 번에 처리해도 되는지.
- 현재 가정: 문서는 두 단계를 개념적으로 분리하고, `dispatch`는 기본적으로 snapshot을 남기지 않는 방향을 택한다.
- trade-off:
  - 분리하면 audit trail이 선명하지만 event 수가 늘어난다.
  - 합치면 운영은 빨라지지만 "왜 닫혔고 왜 넘겼는지"의 경계가 흐려진다.
