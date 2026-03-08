# UI Conventions (MVP)

이 문서는 `unote` MVP의 시각 언어와 공통 UI 규칙을 고정한다.
목표는 화면을 화려하게 꾸미는 것이 아니라, 학습 대상인 영상과 노트 내용이
가장 먼저 읽히는 인터페이스를 일관되게 만드는 것이다.

현재 디자인 방향:

- 브루탈리즘 기반
- 모노톤 중심
- 최소 인터페이스
- 내용 본질 우선

관련 SoT:

- [MVP spec](mvp-spec.md)
- [Sitemap](sitemap.md)
- [Screen spec](screen-spec.md)
- [Frontend routing/state](frontend-routing-and-state.md)

## 1. Visual Direction

### 핵심 인상

- 화면은 "잘 꾸민 대시보드"보다 "날것의 작업면"에 가깝게 느껴져야 한다.
- 정보 카드가 아니라 명확한 블록과 선으로 구획한다.
- 시각적 장식보다 구조와 대비로 긴장을 만든다.
- 깔끔하되 부드럽지 않고, 단정하되 친절하게 과장하지 않는다.

### 피해야 하는 인상

- SaaS 대시보드처럼 둥근 카드와 옅은 그림자를 많이 쓰는 구성
- 여러 강조색으로 상태를 구분하는 구성
- 시각 요소가 노트 본문보다 더 먼저 눈에 들어오는 구성
- 지나치게 많은 설명문, 배지, 보조 텍스트로 밀도를 높이는 구성

## 2. Color Principles

### 기본 원칙

- 색은 의미 전달보다 구조와 대비를 만드는 데 쓴다.
- 기본 팔레트는 흑백과 중간 회색 위주로 제한한다.
- 강조가 필요해도 "강한 원색" 대신 대비 변화로 우선 해결한다.

### MVP 권장 팔레트

- Background: `#f3f3f0` 또는 거의 흰색 계열
- Surface: `#ffffff`
- Primary text: `#111111`
- Secondary text: `#5c5c5c`
- Border: `#111111`
- Muted border: `#cfcfc9`
- Disabled fill: `#e7e7e2`

### 상태 색 사용 규칙

- 기본 상태는 색이 아니라 굵기, 선, 라벨로 구분한다.
- 에러는 제한적으로만 사용한다.
- 성공 색은 남용하지 않는다. 저장 완료는 초록색보다 텍스트와 상태 전환으로 처리한다.
- degraded 상태는 노란 경고색보다 회색 박스 + 명시적 카피를 우선한다.

## 3. Typography

### 원칙

- 본문은 읽기 우선이다.
- 제목은 크기보다 밀도와 무게 차이로 위계를 만든다.
- 타이포 스타일 수는 적게 유지한다.

### 역할 분리

- Heading: 압축감 있는 grotesk/sans 계열
- Body: 장문 읽기에 무리 없는 sans 또는 serif-free 본문체
- Meta, timestamp, code-like 정보: monospace 계열

### 규칙

- `video_id`, timestamp, route-like 메타정보는 monospace로 처리한다.
- 화면마다 다른 폰트 조합을 쓰지 않는다.
- 과한 자간, 장식적 italic, 과도한 uppercase 남용을 피한다.
- 본문 markdown은 읽기 밀도를 유지하기 위해 line length를 제한한다.

## 4. Layout Rules

### 페이지 공통 구조

- 모든 화면은 `Header + Main`의 단순 구조를 기본으로 한다.
- Header는 짧고 단단해야 하며, navigation을 과하게 늘리지 않는다.
- Main은 하나의 핵심 작업면만 강하게 보이게 한다.

### 간격 규칙

- spacing scale은 적은 단계만 사용한다.
- 작은 간격과 큰 간격의 차이를 분명히 둔다.
- 중간 단계가 너무 많아지면 브루탈리즘 긴장감이 약해진다.

권장 단계:

- `8`
- `12`
- `16`
- `24`
- `32`
- `48`

### 경계 표현

- 카드 대신 사각형 블록과 굵은 border를 우선한다.
- 그림자는 기본적으로 쓰지 않는다.
- surface 구분은 배경색보다 border와 여백으로 먼저 해결한다.
- radius는 없거나 아주 작게 유지한다.

## 5. Navigation Conventions

- 글로벌 navigation은 최소로 유지한다.
- 주요 진입점은 `Feed`, `Notes`, `Sources` 정도로 제한한다.
- 현재 위치는 색이 아니라 라벨 무게, underline, border change로 드러낸다.
- breadcrumb는 MVP에서 기본값이 아니다.

## 6. Component Conventions

### Buttons

- primary button은 꽉 찬 검정 또는 거의 검정 배경 + 흰 텍스트
- secondary button은 흰 배경 + 검정 border
- ghost button은 링크처럼 보이되 텍스트 장식은 절제
- 버튼 크기 종류를 과하게 늘리지 않는다.

규칙:

- CTA 우선순위는 한 화면에 명확히 하나만 둔다.
- destructive가 아닌 이상 빨간 filled button을 기본 버튼으로 쓰지 않는다.
- disabled는 흐린 색보다 상호작용 차단이 분명히 보이게 처리한다.

### Inputs

- 입력창은 border가 분명한 사각형으로 둔다.
- placeholder는 설명을 대신하지 않는다.
- helper text는 짧게 유지한다.
- 오류는 input 바로 아래에 붙인다.

### Panels

- panel은 "정보 카드"가 아니라 "작업 영역"처럼 보여야 한다.
- 패널마다 얇은 회색 구분보다 또렷한 외곽선이 더 우선이다.
- 동일 화면에 패널이 너무 많아지면 다시 합친다.

### Lists

- list row는 클릭 가능한 작업 단위로 읽혀야 한다.
- row 안의 정보 우선순위는 제목 또는 핵심 식별자, 그 다음 메타정보다.
- 각 row는 독립 카드처럼 띄우지 않고, 단일 리스트의 연속된 밀도로 보이게 한다.

## 7. State Presentation

### Empty

- empty state는 큰 일러스트 없이 텍스트 중심으로 처리한다.
- 왜 비어 있는지와 다음 행동 하나만 말한다.
- CTA는 하나만 강하게 준다.

### Loading

- skeleton은 과장하지 않는다.
- 레이아웃 뼈대만 보여 주고, shimmer 효과는 기본값이 아니다.
- loading 문구는 짧고 기능 중심으로 쓴다.

### Error

- 에러는 modal보다 inline block이 기본이다.
- 무엇이 실패했고 사용자가 무엇을 다시 할 수 있는지 함께 적는다.
- 시스템 세부 오류를 노출하지 않는다.

### Degraded

- degraded는 실패가 아니라 "핵심은 유지되고 enrichment만 빠진 상태"로 보이게 해야 한다.
- warning tone은 낮게 유지한다.
- row 제거, 영역 collapse, route 이탈로 연결하지 않는다.

## 8. Screen-Specific Guidance

### Source 등록

- 입력과 목록을 한 화면에 두되, 시선의 중심은 입력에 둔다.
- source 목록은 관리 화면이 아니라 "이미 등록된 입력" 확인 영역처럼 다룬다.

### Video Feed

- 영상 목록이 화면의 주인공이어야 한다.
- filter bar는 가볍고 단단하게, 탭처럼 보이게 처리한다.
- "영상 URL로 바로 열기"는 보조 진입점이므로 과도하게 강조하지 않는다.

### Note List

- row는 메타데이터가 없어도 식별 가능해야 한다.
- 제목/썸네일은 enrichment이므로 row 구조를 지배하면 안 된다.
- 수정 시점은 조용하지만 명확하게 드러난다.

### Video Workspace

- 플레이어와 노트가 같은 무게로 싸우지 않게 한다.
- `write`에서는 노트 영역이 slightly dominant해야 한다.
- `read`에서는 읽는 흐름과 timestamp 상호작용이 dominant해야 한다.
- 모드 전환은 탭보다는 blunt한 segmented control에 가깝게 보이게 한다.

## 9. Responsive Rules

### Desktop

- `Video Workspace`는 좌우 분할이 기본이다.
- 왼쪽은 player/context, 오른쪽은 note/work area를 기본으로 한다.
- 한 화면에 3열 이상을 만들지 않는다.

### Mobile

- 상하 분할로 단순화한다.
- sticky 요소를 남용하지 않는다.
- player, mode switch, note 순서가 자연스럽게 이어져야 한다.

### 공통

- 화면이 줄어들어도 정보 종류를 늘리지 않는다.
- 작은 화면에서는 "숨기기"보다 "순서 재배치"를 우선한다.

## 10. Motion Rules

- motion은 최소화한다.
- route 전환, 패널 등장, 저장 상태 전환에만 제한적으로 사용한다.
- 과한 easing, bounce, spring 효과는 피한다.
- note 작성과 읽기 흐름을 방해하는 animation은 금지한다.

## 11. Copy Tone

- 짧고 직접적이어야 한다.
- 과도한 마케팅 문구를 넣지 않는다.
- 사용자를 달래는 표현보다 현재 상태와 다음 행동을 명확히 말한다.

예:

- 좋음: `영상 URL 형식을 확인하세요`
- 나쁨: `문제가 발생했어요. 다시 시도해 보실래요?`

## 12. Implementation Guidance For MVP

- CSS 변수로 색, border, spacing token을 먼저 고정한다.
- radius, shadow, accent color를 기본 디자인 수단으로 삼지 않는다.
- 공통 primitive는 `Button`, `Input`, `Panel`, `ListRow`, `StateBlock` 정도의 작은 집합으로 시작한다.
- 스타일 시스템은 얇게 유지하고, screen-specific override를 최소화한다.

## 13. Non-Goals

- 브랜드 컬러 중심의 감성 UI
- glassmorphism, neumorphism, soft-shadow card UI
- 복잡한 대시보드 레이아웃
- decorative illustration 중심 empty state
- 화려한 micro-interaction

## 14. Revisit When

- 레퍼런스 디자인이 추가로 확정될 때
- 모바일 사용 비중이 높아져 현재 밀도가 너무 높다고 판단될 때
- video workspace에서 player와 note의 우선순위가 실제 사용성 검증과 어긋날 때
