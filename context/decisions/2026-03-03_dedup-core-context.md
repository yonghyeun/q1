# DEC: De-duplicate `product-context` vs `technical-context`

- Date: 2026-03-03
- Context: `context/core/product-context.md`와 `context/core/technical-context.md`에 "Next.js 단일 앱", "DB는 MVP에서 제외" 같은 내용이 중복돼 정본 위치가 흐려질 수 있다.
- Decision: 제품 컨텍스트에서는 기술 스택/구현 범위 언급을 제거하고, 기술 관련 결정(스택/DB 범위/단일 앱 원칙)은 기술 컨텍스트로 수렴한다.
- Alternatives: 두 파일 모두에 요약을 유지한다. 하나의 파일로 합친다.
- Tradeoffs: 제품 문서만 읽었을 때 기술 요약이 바로 보이지 않는다(기술 컨텍스트를 봐야 함). 대신 중복/불일치 리스크를 줄이고 파일 역할이 명확해진다.
- Revisit if: 기술 스택이 커져 `technical-context`가 과도하게 비대해지거나, 제품/기술 경계가 달라질 때.

