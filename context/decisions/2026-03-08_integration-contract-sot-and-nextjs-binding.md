# DEC: Keep integration contracts neutral as SoT, and document Next.js binding separately

- Date: 2026-03-08
- Context: `unote`의 실제 구현 타깃은 Next.js이므로, 에이전트가 바로 route handler와 앱 구조를 이해할 수 있는 문서가 필요하다. 하지만 YouTube 연동 계약을 곧바로 `Next.js API route` 자체로 고정하면, product/contracts 문서가 "무슨 의미를 보장해야 하는가"보다 "어디에 구현하는가"를 먼저 설명하게 된다. 이렇게 되면 SoT 문서가 프레임워크 세부사항에 과하게 묶이고, 나중에 server action, BFF, 별도 proxy로 구현을 옮길 때도 제품 계약 문서를 함께 흔들어야 한다.
- Decision: product/contracts의 YouTube 연동 문서는 implementation-neutral한 integration contract를 SoT로 유지하고, 현재 프로젝트의 구현 바인딩은 별도 명시 레이어로 둔다.
  - SoT 문서는 `resolve channel`, `list channel videos`, `get videos by id`, `parse video url`처럼 앱이 외부와 주고받아야 하는 의미와 성공/실패 해석을 먼저 고정한다.
  - Next.js route handler, server action, proxy/BFF 같은 것은 "현재 구현 바인딩"으로 분리해 기록한다.
  - 현재 MVP의 기본 구현 바인딩은 `apps/web` 내부 Next.js route handler와 `/api/youtube/*` route family를 우선 가정한다.
  - 에이전트가 구현을 시작할 때는 neutral integration contract와 current implementation binding을 함께 읽는 것을 기본으로 한다.
- Alternatives: contracts 자체를 Next.js route contract로 직접 고정한다. 반대로 구현 바인딩을 전혀 기록하지 않고 완전히 추상적인 integration 문서만 유지한다.
- Tradeoffs: 두 층을 같이 관리해야 하므로 문서 구조가 약간 늘어난다. 대신 product SoT는 오래 유지되고, Next.js 구현 에이전트도 현재 route/handler 기준을 즉시 이해할 수 있다. 구현 변경이 생겨도 의미 계약과 프레임워크 바인딩을 독립적으로 갱신할 수 있다는 장점이 있다.
- Revisit if: Next.js가 더 이상 주 구현 타깃이 아니게 되거나, 반대로 프로젝트가 장기간 Next.js에 강하게 고정되어 SoT와 구현 바인딩을 분리할 이점이 거의 없어질 때.
