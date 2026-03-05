# Glossary (Ubiquitous Language, SoT)

이 문서는 `docs/product/*`에서 사용하는 제품 도메인 용어의 Source of Truth(SoT)다.
새 용어를 만들거나 기존 용어가 헷갈릴 때는 이 파일을 먼저 수정한다.

## 원칙

- 엔티티(명사)는 가능하면 영문 용어를 기준으로 한다(코드/이벤트/데이터 모델과 정렬).
- UI 문구는 한국어를 쓰더라도, 아래 정의된 용어를 "개념의 이름"으로 사용한다.
- 같은 개념에 다른 단어를 붙이지 않는다(동의어 남발 금지).

## Entities

### Source

- 정의: 유저가 등록하는 "학습 소스". 이 소스에서 Video 목록을 가져온다.
- MVP: `ChannelSource`만 지원한다.
- 후속: `PlaylistSource` 지원(플레이리스트 기반 학습).

### ChannelSource

- 정의: 유튜브 채널 URL로 등록된 Source.
- 역할: 해당 채널의 업로드 목록에서 Video를 가져온다.

### Video

- 정의: 유튜브 영상 1개(`video_id`로 식별).
- 주의: Video는 Source가 아니다. "영상 URL로 바로 열기(Video URL Open)"는 진입 방식(open method)이다.

### Note

- 정의: Video 1개에 대해 유저가 작성하는 마크다운 노트.
- MVP 제약: `1 Video : 1 Note` (노트 분할/폴더링은 후속).

### Marker

- 정의: Note 안에 삽입되는 타임스탬프 레퍼런스(영상의 특정 시점).
- 저장: `timestamp_seconds`(정수 초)로 저장하고, 표시는 `HH:MM:SS`로 한다.
- 동작: Marker 클릭 시 외부 이동이 아니라 플레이어 `seek`으로 이동한다.

## Views & Flows

### Video Feed

- 정의: 앱 내부에서 보여주는 Video 목록 화면/경험.
- 목적: 유튜브 홈/추천 대신 "학습 세션"을 보호하기 위한 탐색 경로.

### All Feed

- 정의: 유저가 등록한 모든 ChannelSource의 Video를 `publishedAt` 내림차순으로 머지한 통합 피드.
- 구현 메모: 채널별 버퍼를 머지(k-way merge)해 "가상 페이지네이션"을 만든다.

### Channel Filter

- 정의: Video Feed의 범위를 좁히는 상태.
- 값: `All`(기본) 또는 특정 ChannelSource 1개(단일 선택).

### Load older

- 정의: 현재 선택된 Filter 기준으로 더 오래된 Video를 추가로 불러오는 동작.
- UI 라벨(예): "더 보기", "이전 영상 불러오기"
- 기본 단위: 30개씩

### Video URL Open

- 정의: 유저가 유튜브 "영상 URL"을 붙여넣어 특정 Video를 바로 여는 진입 경로.
- 목적: 목록 탐색 없이도 Player + Note의 코어 가치를 즉시 경험하게 한다.

### Player + Note

- 정의: 임베드 플레이어와 마크다운 Note 편집기를 같은 화면에서 제공하는 코어 화면.
- 코어 행동: `timestamp_inserted`(Marker 삽입)과 `timestamp_clicked`(seek 점프).

## Metrics (Product)

### Activation

- 정의(초기): 첫 세션에서 `timestamp_inserted`가 1회 이상 발생한 비율.

### Retention (D1/D7)

- 정의(초기): 동일 유저가 D1/D7에 재방문하는 비율.
- 참고: "재방문"의 의미(예: `video_opened` 또는 `timestamp_inserted`)는 metrics 문서에서 구체화한다.

### Session

- 정의: 유저가 unote에서 학습 목적으로 연속 사용한 시간 구간.
- 참고: 계측 관점의 session cut-off(예: 30분 inactivity)는 analytics 구현에서 정한다.
