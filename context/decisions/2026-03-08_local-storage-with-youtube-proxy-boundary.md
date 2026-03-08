# DEC: Keep local app state in LocalStorage, but use a thin server-side proxy for YouTube integration

- Date: 2026-03-08
- Context: `unote` MVP는 회원가입/로그인 없이 브라우저 LocalStorage를 정본 저장소로 사용하는 방향으로 가고 있다. 동시에 영상 메타데이터, 채널 해석, 채널별 최신 영상 조회는 결국 YouTube Data API를 사용해야 한다. 여기서 LocalStorage만 쓰니 서버 API가 필요 없다고 오해하기 쉽지만, YouTube API key를 브라우저에 직접 노출하면 운영/보안/쿼터 관리 측면의 리스크가 커진다. 또한 source 등록, feed hydrate, note list metadata enrichment, video URL open이 서로 다른 방식으로 YouTube 응답을 해석하면 UI 의미가 쉽게 흔들린다.
- Decision: 앱의 정본 상태는 계속 LocalStorage에 두되, YouTube Data API와의 통신은 얇은 서버 측 proxy/integration boundary를 기본 전제로 둔다.
  - LocalStorage 정본에는 note, source, ui state 같은 유저/앱 내부 데이터만 둔다.
  - YouTube 메타데이터는 정본이 아니라 enrichment 또는 캐시 성격으로 다룬다.
  - YouTube 연동 기능은 product 문서와 contracts에서 "무슨 동작이 필요한가"를 먼저 고정하고, 특정 프레임워크 구현(예: Next.js API route)은 그 다음 단계에서 선택한다.
  - 현재 문서에서 말하는 `resolve channel`, `list channel videos`, `get videos by id`, `parse video url`은 저장 API가 아니라 외부 통합 경계다.
  - 초기 구현은 server DB 없이도 가능하지만, API key를 브라우저에서 직접 사용하지 않도록 thin proxy를 둔다.
- Alternatives: 브라우저에서 YouTube Data API를 직접 호출한다. YouTube 관련 동작도 모두 클라이언트 내부 유틸로만 처리한다. 반대로 note/source 저장까지 포함한 본격 백엔드 서버를 먼저 도입한다.
- Tradeoffs: thin proxy를 두면 구현 경계가 하나 늘고, 에러 정규화와 운영 부담이 약간 생긴다. 대신 API key 노출을 피하고, YouTube 응답을 앱 의미에 맞게 정규화할 수 있으며, LocalStorage 기반 MVP의 단순함은 유지할 수 있다. 또한 나중에 프레임워크나 런타임을 바꾸더라도 integration contract만 유지하면 product contract를 덜 흔들 수 있다.
- Revisit if: YouTube 연동 없이도 MVP 핵심 가치를 검증할 수 있다고 판단될 때. 또는 브라우저 직접 호출이 정책/보안/운영 측면에서 충분히 감당 가능하다고 확인될 때. 혹은 LocalStorage 제약을 넘어서 사용자 데이터 동기화/공유가 필요해져 본격 백엔드가 정본 저장소를 맡게 될 때.
