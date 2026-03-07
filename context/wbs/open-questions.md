# WBS Open Questions

이 문서는 이름과 달리 2026-03-07 기준으로 합의가 끝난 쟁점을 기록한다.
상세 배경과 trade-off는 `../decisions/2026-03-07_wbs-run-ledger-scope-and-decision-boundaries.md`에 남긴다.

## 1. Run ledger가 어떤 slice까지 포함할 것인가

- 결정: `run ledger.slice_entries`는 **runtime artifact가 이미 발행된 slice만** 포함한다.
- 운영 규칙:
  - ledger entry는 첫 packet 발행 또는 그와 동치인 첫 dispatch 시점부터 생성한다.
  - `planned`/`ready` backlog는 WBS가 SoT로 관리하고, run ledger는 runtime control-plane만 다룬다.
  - backlog와 active work를 함께 보고 싶으면 ledger를 확장하지 말고 별도 projection/view를 만든다.
- 이유:
  - 현재 schema가 `current_packet_id`, `latest_trace_id`, `latest_decision_id`를 필수로 요구하므로 runtime 참조가 없는 slice를 넣으면 모델 경계가 흐려진다.
  - validator가 단순해지고 `current state projection`이라는 ledger의 역할이 선명해진다.

## 2. `accept`와 `dispatch`를 항상 분리할 것인가

- 결정: `accept`와 `dispatch`는 **항상 별도 operator decision/event**로 남긴다.
- 운영 규칙:
  - `accept`는 현재 packet을 닫거나 handoff 목적 충족을 승인하는 decision이다.
  - `dispatch`는 다음 actor packet을 발행하는 decision이며 `next_packet_id`를 이 event가 소유한다.
  - operator UX에서 한 번에 처리하더라도 artifact는 `accept` seq N, `dispatch` seq N+1로 분리 기록한다.
  - `accept`는 snapshot checkpoint 대상이고, `dispatch`는 기본적으로 current ledger만 갱신한다.
- 이유:
  - "왜 현재 packet을 닫았는가"와 "왜 다음 actor에게 넘겼는가"의 audit 경계를 보존할 수 있다.
  - 다음 packet 준비가 늦어지는 정상적인 중간 상태를 모델에 그대로 표현할 수 있다.
