# DEC: WBS uses abstract ownership and verification boundaries

- Date: 2026-03-07
- Context: WBS에 `owned_paths`, `required_tests` 같은 concrete runtime detail을 직접 적을지 검토했다. 기존 문서 일부는 WBS 준비 조건을 그렇게 읽힐 수 있게 쓰여 있었지만, `planned flow`가 추가된 뒤에는 WBS와 runtime packet 사이에 한 단계 더 명확한 레이어가 생겼다. 탐색과 설계가 아직 진행 중인 slice에서 file path와 test command를 너무 일찍 고정하면 쉽게 stale해지고, 실제 운영에서는 packet 생성 시점에 node 목적과 최신 입력을 반영해 더 정확한 concrete handoff를 만드는 편이 자연스럽다.
- Decision: WBS는 concrete `owned_paths`, `required_tests`를 직접 정본으로 갖지 않고 `owned_scope`, `verification_requirements` 수준의 추상 경계를 가진다.
  - WBS는 목표, acceptance criteria, contract 경계, ownership boundary, verification obligation의 SoT다.
  - planned flow는 WBS의 추상 경계를 node별 packet blueprint로 분해한다.
  - packet은 현재 node 기준 concrete `owned_paths`, `required_tests`, `inputs`를 채운다.
  - trace는 실제 변경 파일과 실제 실행 테스트를 기록한다.
  - WBS가 orchestration-ready인지 판단할 때도 concrete path/test가 아니라 추상 boundary와 evidence requirement의 충분성을 본다.
- Alternatives: WBS에서 처음부터 정확한 file path와 테스트 명령을 고정하는 waterfall형 계획을 유지한다. 반대로 WBS에는 경계 정보조차 최소화하고 대부분의 판단을 packet 생성 시점 operator 재량에 맡긴다.
- Tradeoffs: 추상 경계 방식은 WBS를 더 가볍고 오래 살아남는 planning SoT로 유지하게 해 주지만, packet 이전 단계에서 exact file/test 목록을 즉시 보장하지는 않는다. 반대로 concrete detail을 늦게 바인딩함으로써 탐색 중 stale planning을 줄이고, WBS 변경과 packet 변경을 다른 레이어에서 추적할 수 있다. 또한 operator가 packet 생성 시 planned flow와 최신 trace를 반영해 node 목적에 맞는 concrete handoff를 만들기 쉬워진다.
- Revisit if: 프로젝트 구조와 테스트 하네스가 장기간 안정돼 대부분의 slice에서 concrete path/test를 미리 고정해도 stale 비용이 거의 없다고 확인되거나, 반대로 `owned_scope`와 `verification_requirements`가 지나치게 추상적이라 packet 단계에서 반복적으로 boundary drift를 유발해 더 강한 planning artifact가 필요해질 때.
