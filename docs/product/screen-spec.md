# Screen Spec (MVP)

이 문서는 WBS slice를 기준으로 MVP 화면별 UX contract를 고정한다.
컴포넌트 구현 디테일이 아니라, 각 화면이 어떤 상태와 행동을 제공해야 하는지를 정의한다.

관련 상위 문서:
- [Sitemap](sitemap.md)
- [MVP spec](mvp-spec.md)
- [Glossary](glossary.md)

## Screen Matrix

| Screen | Route | 핵심 가치 | 관련 slice |
|---|---|---|---|
| Source 등록 | `/sources` | 학습 source를 등록해 피드의 입력을 만든다. | [MVP-SOURCE-ADD-CHANNEL](../../context/wbs/tasks/MVP-SOURCE-ADD-CHANNEL.yaml) |
| Video Feed | `/feed` | 등록 채널의 영상을 앱 내부에서 탐색하고 `write` 진입을 시작한다. | [MVP-VIDEO-FEED-LATEST-LIST](../../context/wbs/tasks/MVP-VIDEO-FEED-LATEST-LIST.yaml), [MVP-VIDEO-FEED-CHANNEL-FILTER](../../context/wbs/tasks/MVP-VIDEO-FEED-CHANNEL-FILTER.yaml), [MVP-VIDEO-FEED-LOAD-OLDER](../../context/wbs/tasks/MVP-VIDEO-FEED-LOAD-OLDER.yaml), [MVP-VIDEO-OPEN-FROM-FEED](../../context/wbs/tasks/MVP-VIDEO-OPEN-FROM-FEED.yaml), [MVP-VIDEO-OPEN-BY-URL](../../context/wbs/tasks/MVP-VIDEO-OPEN-BY-URL.yaml) |
| Note List | `/notes` | 작성한 note가 있는 영상을 다시 찾고 `read` 재진입을 시작한다. | [MVP-NOTE-LIST-BY-UPDATED-AT](../../context/wbs/tasks/MVP-NOTE-LIST-BY-UPDATED-AT.yaml), [MVP-NOTE-LIST-METADATA-ENRICHMENT](../../context/wbs/tasks/MVP-NOTE-LIST-METADATA-ENRICHMENT.yaml), [MVP-VIDEO-OPEN-FROM-NOTE-LIST](../../context/wbs/tasks/MVP-VIDEO-OPEN-FROM-NOTE-LIST.yaml) |
| Video Write | `/videos/[video_id]/write` | 영상 보면서 노트를 작성하고 타임스탬프를 삽입한다. | [MVP-PLAYER-NOTE-WORKSPACE](../../context/wbs/tasks/MVP-PLAYER-NOTE-WORKSPACE.yaml), [MVP-NOTE-LOCAL-PERSISTENCE](../../context/wbs/tasks/MVP-NOTE-LOCAL-PERSISTENCE.yaml), [MVP-TS-INSERT](../../context/wbs/tasks/MVP-TS-INSERT.yaml) |
| Video Read | `/videos/[video_id]/read` | 같은 노트를 읽기 중심으로 보고 timestamp click seek으로 복습한다. | [MVP-PLAYER-NOTE-WORKSPACE](../../context/wbs/tasks/MVP-PLAYER-NOTE-WORKSPACE.yaml), [MVP-NOTE-LOCAL-PERSISTENCE](../../context/wbs/tasks/MVP-NOTE-LOCAL-PERSISTENCE.yaml), [MVP-TIMESTAMP-CLICK-SEEK](../../context/wbs/tasks/MVP-TIMESTAMP-CLICK-SEEK.yaml) |

## 1. Source 등록

### 목적

- 사용자가 채널 URL을 등록해 이후 `Video Feed`의 입력 source를 만든다.
- 이미 등록된 source를 확인할 수 있게 한다.

### 주요 영역

- 페이지 헤더
- 채널 URL 입력 필드
- `등록` primary action
- 입력 검증/에러 메시지 영역
- 등록된 source 목록
- `/feed`로 이동하는 CTA

### 주요 행동

- 채널 URL 입력
- 등록 실행
- 중복/유효성 오류 확인
- 등록된 source 목록 확인
- 피드 화면으로 이동

### 상태

#### Empty

- 등록된 source가 하나도 없을 때
- 입력 필드와 등록 CTA를 기본적으로 노출한다.
- `학습할 채널을 먼저 등록하세요` 성격의 안내와 `/feed` 대신 source 등록에 집중하는 메시지를 쓴다.

#### Validating

- 채널 URL 해석/검증 중일 때
- 중복 제출을 막기 위해 등록 CTA를 일시적으로 비활성화한다.

#### Invalid Input

- 지원하지 않는 채널 URL 형식이거나 해석 실패 시
- 입력 필드 근처에 인라인 에러를 보여 주고 등록은 완료되지 않는다.

#### Duplicate

- 이미 등록된 source와 같은 채널일 때
- 새 source를 만들지 않고 중복 안내를 보여 준다.

#### Registered List

- 하나 이상 등록된 source가 있을 때
- 등록된 채널의 최소 식별 정보와 함께 목록을 보여 준다.
- `피드 보러 가기` CTA를 노출한다.

### 화면 경계 메모

- 이 화면은 source 생성과 목록 확인까지만 책임진다.
- 영상 피드 탐색이나 영상 URL open은 이 화면의 1차 책임이 아니다.

## 2. Video Feed

### 목적

- 등록 채널 기반 최신 영상 목록을 보여 준다.
- `All` 또는 특정 채널 1개로 범위를 좁힌다.
- 영상 선택 또는 영상 URL 붙여넣기를 통해 `Video Write`로 이동시킨다.

### 주요 영역

- 페이지 헤더
- `영상 URL로 바로 열기` 입력 surface
- `All` / 채널 단일 선택 filter bar
- 영상 목록
- `Load older` CTA
- empty/loading/degraded 상태 영역

### 주요 행동

- 기본 `All` 피드 열람
- 채널 필터 전환
- 피드 항목 선택
- `Load older` 실행
- 영상 URL 붙여넣기 후 명시적 `열기` 실행

### 상태

#### No Source Empty

- 등록된 source가 없을 때
- 피드 목록 대신 source 등록 CTA를 보여 준다.
- 같은 화면 안에서 "영상 URL로 바로 열기" surface는 계속 노출한다.

#### Initial Loading

- 기본 피드를 처음 계산하는 동안
- filter bar와 목록 영역은 skeleton 또는 loading state를 보여 준다.

#### Ready: All

- 등록 채널 영상이 `published_at` 기준으로 정렬되어 보인다.
- 기본 필터는 `All`이다.

#### Ready: Single Channel

- 사용자가 특정 채널을 선택한 상태다.
- 목록과 `Load older`는 현재 선택된 채널 범위만 따른다.

#### Load Older Pending

- `Load older` 요청 중
- 기존 목록은 유지하고 CTA만 pending 상태로 바꾼다.

#### Partial/Degraded Load

- 일부 채널 메타데이터 조회나 추가 fetch에 실패했지만 피드 전체를 완전히 닫지 않을 때
- 목록은 가능한 범위까지만 보여 주고, 상단 또는 목록 근처에 비치명적 경고를 둔다.

#### URL Open Invalid

- 영상 URL 파싱이 실패했을 때
- URL 입력 surface 주변에 인라인 에러를 보여 준다.

### 화면 경계 메모

- "영상 URL로 바로 열기"는 이 화면의 보조 surface다.
- feed filter 상태는 현재 세션의 탐색 컨텍스트로만 다루고, fresh entry 시 기본값은 `All`이다.
- 검색, 추천, 무한 스크롤은 MVP 범위 밖이다.

## 3. Note List

### 목적

- 저장된 note가 있는 영상을 다시 찾는 재진입 surface를 제공한다.
- 목록에서 선택한 영상의 `read` 진입을 시작한다.

### 주요 영역

- 페이지 헤더
- note list row 목록
- row 메타데이터 영역(제목/썸네일/수정 시점)
- empty/degraded 상태 영역

### 주요 행동

- 최근 수정한 note 목록 열람
- note row 선택
- `Video Read`로 이동

### 상태

#### No Note Yet

- 저장된 note가 하나도 없을 때
- empty state와 `/feed` CTA를 보여 준다.

#### Ready: Core List

- note가 존재하는 `video_id` row가 note `updated_at` 최신순으로 보인다.
- 메타데이터가 없더라도 `video_id`와 수정 시점으로 row를 식별할 수 있어야 한다.

#### Metadata Hydrating

- 제목/썸네일을 보강하는 중일 때
- row 정렬과 열기 action은 유지하고, 제목/썸네일만 skeleton 또는 placeholder 상태로 둔다.

#### Metadata Degraded

- 제목/썸네일 조회에 실패했거나 unavailable video라서 enrichment가 완전하지 않을 때
- fallback title 또는 `video_id`, placeholder 썸네일, 수정 시점을 유지한다.
- row 선택과 `Video Read` 진입은 막지 않는다.

### 화면 경계 메모

- 이 화면의 정본은 LocalStorage의 note index다.
- 제목/썸네일은 enrichment이고 row 존재 여부를 결정하지 않는다.
- 기본 재진입 route는 `/videos/[video_id]/read`다.

## 4. Shared Video Workspace Rules

### 목적

- `Video Write`와 `Video Read`가 같은 `video_id`와 note SoT를 공유하도록 shell contract를 고정한다.

### 공통 영역

- 화면 상단의 최소 컨텍스트 바
- mode switch
- YouTube 임베드 플레이어 영역
- 노트 영역
- 비정상 상태 알림 영역

### 공통 레이아웃 규칙

- 데스크톱 기본값은 좌우 분할이다.
- 모바일 기본값은 상하 분할이다.
- 플레이어 위 오버레이 UI는 두지 않는다.
- 노트는 별도 팝업이나 새 창으로 분리하지 않는다.
- `write/read` 전환은 route만 바꾸고 가능한 한 같은 video workspace 맥락을 유지한다.

### 공통 상태

#### Video Initializing

- 플레이어가 초기화 중일 때
- 플레이어 영역은 loading 상태를 보이고 노트 영역 전체를 hard-block하지 않는다.

#### Invalid or Unavailable Video

- `video_id`가 잘못됐거나 플레이어 초기화가 불가능할 때
- 플레이어 영역에 오류 상태를 보여 주고 `/feed`로 돌아갈 수 있는 CTA를 제공한다.

### 공통 경계 메모

- stable entity key는 `video_id`다.
- `/videos/[video_id]`는 `/videos/[video_id]/write`로 redirect한다.
- `write`와 `read`는 별도 route지만 같은 노트 데이터와 플레이어 컨텍스트를 공유한다.

## 5. Video Write

### 목적

- `video_id` 기준으로 영상 재생과 노트 편집을 함께 수행한다.
- 현재 재생 시점 타임스탬프 삽입과 로컬 자동저장을 담당한다.

### 주요 영역

- write/read mode switch
- 편집 가능한 노트 영역
- 타임스탬프 삽입 진입점
- 로컬 저장 상태 표시
- `read`로 이동하는 전환 action

### 주요 행동

- 기존 노트 불러오기 또는 새 노트 시작
- 노트 편집
- 현재 재생 시점 타임스탬프 삽입
- `read` mode로 전환

### 상태

#### Empty Note

- 현재 `video_id`에 저장된 노트가 없을 때
- 빈 편집 영역을 보여 주고 즉시 작성 가능해야 한다.

#### Existing Note

- 현재 `video_id`에 기존 노트가 있을 때
- 마지막 저장 결과를 복원해 편집을 이어갈 수 있어야 한다.

#### Local Save Pending

- 입력 후 자동저장이 반영 중일 때
- 편집은 계속 가능해야 하며, blocking modal은 두지 않는다.

#### Local Save Degraded

- LocalStorage 접근 문제나 저장 실패가 발생했을 때
- 편집은 가능한 한 유지하되, 노트가 안전하게 보존되지 않을 수 있음을 비치명적 경고로 보여 준다.

### 화면 경계 메모

- feed 또는 URL open의 기본 landing route는 `/videos/[video_id]/write`다.
- edit intent가 있는 surface만 이 route로 진입시킨다.
- timestamp 삽입은 이 route의 책임이다.

## 6. Video Read

### 목적

- 같은 `video_id`의 노트를 읽기 중심으로 보여 준다.
- timestamp click seek으로 복습 행동을 닫는다.

### 주요 영역

- write/read mode switch
- 읽기 전용 노트 렌더링 영역
- timestamp click target
- `write`로 이동하는 전환 action

### 주요 행동

- 기존 노트 읽기
- 노트 안 timestamp 클릭 후 seek
- `write` mode로 전환

### 상태

#### No Note Yet

- 현재 `video_id`에 아직 노트가 없을 때
- 비어 있는 read surface 대신 `아직 노트가 없습니다` 안내와 `write`로 이동하는 CTA를 보여 준다.

#### Rendered Note

- 현재 `video_id`의 노트가 렌더링 가능한 상태일 때
- timestamp link는 외부 이동이 아니라 seek 대상이어야 한다.

#### Read Render Degraded

- 저장된 노트는 있지만 read renderer나 timestamp binding이 완전하지 않을 때
- 텍스트는 최대한 유지해 보여 주고, 상호작용 제약을 비치명적으로 알린다.

### 화면 경계 메모

- timestamp click seek은 이 route의 책임이다.
- read mode는 노트를 수정하지 않는 것을 기본값으로 한다.
- note가 없는 경우 자동으로 빈 editor를 띄우지 않고 `write` CTA로 전환한다.

## Cross-Screen Rules

- Primary creation flow는 `Source 등록 -> Video Feed -> Video Write -> Video Read`의 순서를 갖는다.
- Primary revisit flow는 `Note List -> Video Read -> Video Write`의 순서를 갖는다.
- root 진입은 `/feed`로 고정한다.
- `/notes`는 source 유무와 무관하게 접근 가능해야 한다.
- `/videos/[video_id]`는 `/videos/[video_id]/write`로 redirect한다.
- `/videos/[video_id]/write`와 `/videos/[video_id]/read` 사이 전환은 같은 `video_id`를 유지한다.
- `Note List` row 선택의 기본 landing route는 `/videos/[video_id]/read`다.
- video workspace 안에서 뒤로 가면 browser history를 우선한다.
- 새 세션에서 `Video Feed`에 진입했을 때 filter 기본값은 `All`이다.
- `Video Feed`의 URL open은 붙여넣기 즉시 실행이 아니라 명시적 `열기` action을 기본값으로 한다.
