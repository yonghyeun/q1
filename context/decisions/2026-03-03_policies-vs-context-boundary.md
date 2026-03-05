# DEC: Keep policies in `policies/`, avoid duplication in `context/core/`

- Date: 2026-03-03
- Context: `context/core/`에 운영 관련 문장이 쌓이면서, `policies/`에 있는 규범(품질/보안/보관)과 역할이 겹쳐 "정본이 어디인지"가 불명확해질 수 있다.
- Decision: 운영 규칙/게이트의 정본은 `policies/`에만 둔다. `context/core/`는 현재 운영 컨텍스트와 정책 포인터만 유지하고, 정책 요약/중복 본문은 최소화한다.
- Alternatives: `context/core/`에 정책 요약을 계속 유지한다. 정책을 전부 `context/`로 이동한다.
- Tradeoffs: `context/core/`만 읽고는 규칙을 완전히 알기 어렵다(포인터를 따라가야 함). 대신 정책 변경이 한 곳에서만 일어나고, 중복/불일치 리스크가 줄어든다.
- Revisit if: 운영 체계가 커져 정책을 별도 사이트로 발행하거나 ADR로 승격해야 할 때, 혹은 `policy-routing`이 과도하게 복잡해질 때.

