# YouTube API 정책 체크 노트 (unote MVP)

> 목적: unote MVP가 YouTube API Services(YouTube Data API + Embedded Player)를 사용하면서 정책과 충돌할 수 있는 지점을 미리 식별하고, 제품/구현 결정을 안전한 범위로 가이드한다.
>
> 주의: 이 문서는 법률 자문이 아니다. 정책은 변경될 수 있으므로, 출시/유료화/스코프 확장 시점에 원문을 다시 확인한다.

## 기준 문서(원문, SoT)

- YouTube API Services Developer Policies: https://developers.google.com/youtube/terms/developer-policies
- Developer Policies Guide: https://developers.google.com/youtube/terms/developer-policies-guide?hl=ko
- Required Minimum Functionality: https://developers.google.com/youtube/terms/required-minimum-functionality
- Branding Guidelines: https://developers.google.com/youtube/terms/branding-guidelines
- YouTube API Services Terms of Service: https://developers.google.com/youtube/terms/api-services-terms-of-service

## unote MVP와 직접 관련 있는 “위험 구간”

### 1) 플레이어 UI/동작 변경(커스텀 플레이어, 오버레이, 광고/기능 차단)

unote는 “Player + Note” 한 화면이 핵심이라, **플레이어 위에 무언가를 겹치거나(오버레이) 기본 UI를 숨기는** 방향으로 쉽게 흘러갈 수 있다.

정책적으로 안전하게 가려면:

- **임베드 플레이어 위에 UI(버튼/노트/가이드/툴팁)를 겹치지 않는다.**
  - 노트/버튼은 플레이어 “옆” 또는 “아래” 레이아웃으로 분리한다.
- **플레이어의 기본 기능/브랜딩/광고를 막거나 변경하지 않는다.**
  - “관련 영상/설정 휠/전체화면/자막 등” 사용자가 기대하는 기본 경험을 제한하지 않는 방향으로 UX를 설계한다.
- **문서에 명시된 범위(공식 파라미터/플레이어 API) 밖의 조작은 하지 않는다.**

### 2) PiP(화면 밖 재생) / Background play

MVP에서 PiP를 “우리 앱 기능”으로 제공하고 싶어질 수 있다.

정책 리스크 관점에서:

- YouTube는 “background player”를 금지 대상으로 명시하고 있고, “창이 닫히거나 최소화돼도 재생” 같은 형태를 문제 예시로 든다.
- 따라서 **커스텀 PiP/백그라운드 재생을 제품 기능으로 구현하는 것은 고위험**으로 간주한다.

권장:

- MVP에서는 **PiP/백그라운드 재생을 구현하지 않는다.**
- 사용자가 플랫폼/YouTube 플레이어가 제공하는 기능을 “자연스럽게 사용”하는 수준(통제/우회 없이)으로만 둔다.

### 3) 데이터 저장/캐시(LocalStorage 포함)

unote는 “브라우저 로컬 저장(LocalStorage)”를 MVP 제약으로 두고 있다.

여기서 주의할 점:

- YouTube API로 받은 **API Data(영상 메타데이터 등)**는 “무기한 저장”이 안전하지 않다.
- (로그인 없는) public 데이터 중심의 사용이라면 보통 “Non-Authorized Data” 취급이 되고, 이 경우 **저장 기간/갱신(예: 30일) 제한**이 걸릴 수 있다.

권장 구현 방향:

- LocalStorage에는 가급적 **유저가 만든 데이터(Note/Marker) + 최소 식별자(video_id/channel_id)**만 장기 저장한다.
- 썸네일/타이틀/조회수 같은 메타데이터는
  - “짧은 TTL 캐시”로 취급하거나
  - “항상 최신 fetch”하는 쪽으로 설계한다.

### 4) 유료화(나중에 구독/결제)

원칙:

- **API Client(앱) 자체를 판매/구독 모델로 운영하는 것은 가능**한 범주에 들어갈 수 있다.
- 하지만 **YouTube에서 무료로 제공되는 ‘시청’ 자체를 유료로 판매하거나**, 임베드 플레이어에서 **시청을 유료로 막는 형태**는 위험하다.

권장 유료화 포지셔닝:

- “유튜브를 보여주는 것”이 아니라 **노트/리뷰/정리/검색/내 학습 기록** 같은 **부가가치 기능**에 과금한다.
- 영상 재생 자체는 YouTube 플레이어의 정상 경험으로 제공하고, **재생을 결제 장벽 뒤에 두지 않는다.**

### 5) 피드/썸네일/메타데이터 표시(변형 금지, 독립적 가치)

unote의 “채널 기반 피드”는 YouTube API Data를 많이 표시하게 된다.

가이드:

- 썸네일/타이틀 같은 **메타데이터는 보이게, 그리고 변형 없이** 사용하는 것이 안전하다.
- YouTube 데이터만 나열하는 “복제 클라이언트”가 되지 않도록, 화면이 **노트/학습 컨텍스트 같은 독립적 가치**를 제공하도록 설계한다.

## 제품/설계 결론(현재 unote MVP 기준)

- Player + Note는 “한 화면”이되 **플레이어 영역 위 오버레이는 금지**(좌우 분할/상하 분할로 해결).
- “집중 모드”는 **YouTube 플레이어 기능을 차단해서 구현하지 않는다.**
  - 대신 앱 UI에서 산만함을 줄이는 방향(피드 큐레이션, 단축키, 노트 플로우)을 강화한다.
- PiP/백그라운드 재생은 MVP에서 하지 않는다.
- API Data 캐시는 장기 저장하지 않고, 저장해도 TTL/갱신을 설계한다.
- 유료화는 “노트/학습 경험”에 과금하고, “시청”을 과금하지 않는다.

## 오픈 질문(스코프 확장 시 재검토)

- “검색”을 unote 내부에서 제공할 때(영상/노트) YouTube 정책상 UX/표시 요구사항을 추가로 만족해야 하는지?
- 모바일 앱(PWA/네이티브)로 갈 때 “링크는 YouTube 앱으로 열기” 요구사항을 어떻게 해석/적용할지?
- Data API quota 확장/감사(compliance audit) 대응을 위한 최소 운영 문서/체크리스트는 무엇인지?
