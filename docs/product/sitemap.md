# Sitemap (MVP)

이 문서는 WBS slice를 기준으로 `unote` MVP의 화면 구조와 라우트 계약을 고정한다.
목표는 공통 video workspace shell 위에서 `write/read` 모드를 분리하면서도 코어 플로우와 escape hatch를 흔들리지 않게 유지하는 것이다.

주요 입력:
- [MVP spec](mvp-spec.md)
- [MVP-SOURCE-ADD-CHANNEL](../../context/wbs/tasks/MVP-SOURCE-ADD-CHANNEL.yaml)
- [MVP-VIDEO-FEED-LATEST-LIST](../../context/wbs/tasks/MVP-VIDEO-FEED-LATEST-LIST.yaml)
- [MVP-VIDEO-FEED-CHANNEL-FILTER](../../context/wbs/tasks/MVP-VIDEO-FEED-CHANNEL-FILTER.yaml)
- [MVP-VIDEO-FEED-LOAD-OLDER](../../context/wbs/tasks/MVP-VIDEO-FEED-LOAD-OLDER.yaml)
- [MVP-VIDEO-OPEN-FROM-FEED](../../context/wbs/tasks/MVP-VIDEO-OPEN-FROM-FEED.yaml)
- [MVP-VIDEO-OPEN-BY-URL](../../context/wbs/tasks/MVP-VIDEO-OPEN-BY-URL.yaml)
- [MVP-PLAYER-NOTE-WORKSPACE](../../context/wbs/tasks/MVP-PLAYER-NOTE-WORKSPACE.yaml)
- [MVP-NOTE-LOCAL-PERSISTENCE](../../context/wbs/tasks/MVP-NOTE-LOCAL-PERSISTENCE.yaml)
- [MVP-NOTE-LIST-BY-UPDATED-AT](../../context/wbs/tasks/MVP-NOTE-LIST-BY-UPDATED-AT.yaml)
- [MVP-NOTE-LIST-METADATA-ENRICHMENT](../../context/wbs/tasks/MVP-NOTE-LIST-METADATA-ENRICHMENT.yaml)
- [MVP-TS-INSERT](../../context/wbs/tasks/MVP-TS-INSERT.yaml)
- [MVP-TIMESTAMP-CLICK-SEEK](../../context/wbs/tasks/MVP-TIMESTAMP-CLICK-SEEK.yaml)
- [MVP-VIDEO-OPEN-FROM-NOTE-LIST](../../context/wbs/tasks/MVP-VIDEO-OPEN-FROM-NOTE-LIST.yaml)

## 원칙

- MVP의 user-facing route surface는 `Source 등록`, `Video Feed`, `Note List`, `Video Write`, `Video Read` 5개로 본다.
- `Video Write`와 `Video Read`는 같은 `video_id`를 공유하는 video workspace shell 위에서 동작한다.
- `Note List`는 로컬 note 정본에서 파생되는 재진입 surface이며, 메타데이터가 없어도 동작해야 한다.
- "영상 URL로 바로 열기"는 별도 페이지가 아니라 `Video Feed` 안의 escape hatch surface로 둔다.
- canonical video route family는 `/videos/[video_id]/*`이고, 안정적으로 소유하는 식별자는 `video_id`다.
- `/videos/[video_id]`는 entry route이며 `/videos/[video_id]/write`로 redirect한다.
- `feed_filter`, `filter_source_id`, `open_method` 같은 맥락은 analytics/navigation 입력이지 canonical URL의 일부가 아니다.
- 루트 진입점은 빠른 가치 경험을 위해 `Video Feed`로 정한다.

## Route Map

| Route | Screen | 목적 | 관련 slice |
|---|---|---|---|
| `/` | Entry redirect | 앱 첫 진입점을 `Video Feed`로 정렬한다. | [MVP-VIDEO-FEED-LATEST-LIST](../../context/wbs/tasks/MVP-VIDEO-FEED-LATEST-LIST.yaml), [MVP-VIDEO-OPEN-BY-URL](../../context/wbs/tasks/MVP-VIDEO-OPEN-BY-URL.yaml) |
| `/sources` | Source 등록 화면 | 채널 URL 등록과 등록된 source 확인을 담당한다. | [MVP-SOURCE-ADD-CHANNEL](../../context/wbs/tasks/MVP-SOURCE-ADD-CHANNEL.yaml) |
| `/feed` | Video Feed 화면 | 등록 채널 기반 영상 탐색, 필터, `Load older`, 영상 URL open surface를 제공한다. | [MVP-VIDEO-FEED-LATEST-LIST](../../context/wbs/tasks/MVP-VIDEO-FEED-LATEST-LIST.yaml), [MVP-VIDEO-FEED-CHANNEL-FILTER](../../context/wbs/tasks/MVP-VIDEO-FEED-CHANNEL-FILTER.yaml), [MVP-VIDEO-FEED-LOAD-OLDER](../../context/wbs/tasks/MVP-VIDEO-FEED-LOAD-OLDER.yaml), [MVP-VIDEO-OPEN-FROM-FEED](../../context/wbs/tasks/MVP-VIDEO-OPEN-FROM-FEED.yaml), [MVP-VIDEO-OPEN-BY-URL](../../context/wbs/tasks/MVP-VIDEO-OPEN-BY-URL.yaml) |
| `/notes` | Note List 화면 | 작성한 note가 있는 영상을 다시 찾고 read mode 재진입을 시작한다. | [MVP-NOTE-LIST-BY-UPDATED-AT](../../context/wbs/tasks/MVP-NOTE-LIST-BY-UPDATED-AT.yaml), [MVP-NOTE-LIST-METADATA-ENRICHMENT](../../context/wbs/tasks/MVP-NOTE-LIST-METADATA-ENRICHMENT.yaml), [MVP-VIDEO-OPEN-FROM-NOTE-LIST](../../context/wbs/tasks/MVP-VIDEO-OPEN-FROM-NOTE-LIST.yaml) |
| `/videos/[video_id]` | Video workspace entry | stable `video_id` route를 소유하고 기본 write mode로 보낸다. | [MVP-PLAYER-NOTE-WORKSPACE](../../context/wbs/tasks/MVP-PLAYER-NOTE-WORKSPACE.yaml) |
| `/videos/[video_id]/write` | Video Write 화면 | 플레이어와 편집 가능한 노트를 같은 화면에서 열고 기록 행동을 수행한다. | [MVP-PLAYER-NOTE-WORKSPACE](../../context/wbs/tasks/MVP-PLAYER-NOTE-WORKSPACE.yaml), [MVP-NOTE-LOCAL-PERSISTENCE](../../context/wbs/tasks/MVP-NOTE-LOCAL-PERSISTENCE.yaml), [MVP-TS-INSERT](../../context/wbs/tasks/MVP-TS-INSERT.yaml), [MVP-VIDEO-OPEN-FROM-FEED](../../context/wbs/tasks/MVP-VIDEO-OPEN-FROM-FEED.yaml), [MVP-VIDEO-OPEN-BY-URL](../../context/wbs/tasks/MVP-VIDEO-OPEN-BY-URL.yaml) |
| `/videos/[video_id]/read` | Video Read 화면 | 같은 노트를 읽기 중심으로 보여 주고 timestamp click seek으로 복습한다. | [MVP-PLAYER-NOTE-WORKSPACE](../../context/wbs/tasks/MVP-PLAYER-NOTE-WORKSPACE.yaml), [MVP-NOTE-LOCAL-PERSISTENCE](../../context/wbs/tasks/MVP-NOTE-LOCAL-PERSISTENCE.yaml), [MVP-TIMESTAMP-CLICK-SEEK](../../context/wbs/tasks/MVP-TIMESTAMP-CLICK-SEEK.yaml), [MVP-VIDEO-OPEN-FROM-NOTE-LIST](../../context/wbs/tasks/MVP-VIDEO-OPEN-FROM-NOTE-LIST.yaml) |

## Entry Rules

### `/`

- 첫 진입 시 `/feed`로 보낸다.
- 등록된 source가 없더라도 `/feed`는 접근 가능해야 한다.
- source가 없는 경우 `Video Feed`는 empty state를 보여 주고 `Source 등록` CTA와 "영상 URL로 바로 열기" surface를 함께 제공한다.

### `/sources`

- 채널 URL 등록의 정식 화면이다.
- 등록 성공 후 자동 redirect를 강제하지 않는다.
- 대신 `피드 보러 가기` CTA를 제공해 `/feed`로 이동할 수 있게 한다.

### `/feed`

- 앱의 기본 탐색 화면이다.
- source가 있으면 기본 `All` 피드가 보인다.
- source가 없으면 empty state가 보인다.
- 영상 URL open은 이 화면 상단의 보조 입력 surface로 둔다.

### `/notes`

- 저장된 note가 하나 이상 있으면 `updated_at` 최신순 목록을 보여 준다.
- 저장된 note가 없으면 empty state와 `/feed` 이동 CTA를 보여 준다.
- 제목/썸네일은 best-effort enrichment다.
- 메타데이터가 없거나 실패해도 row는 `video_id`와 수정 시점 기반 fallback으로 유지되고 열기 행동은 계속 가능해야 한다.

### `/videos/[video_id]`

- video workspace의 canonical entry route다.
- stable route contract는 path param `video_id` 하나다.
- 이 route 자체는 화면 모드를 소유하지 않고 `/videos/[video_id]/write`로 보낸다.

### `/videos/[video_id]/write`

- 영상 기록의 기본 진입 route다.
- feed에서 열기와 URL로 열기는 모두 이 route로 수렴한다.
- 노트가 이미 있어도 우선 write mode로 진입한다.

### `/videos/[video_id]/read`

- 같은 `video_id`의 노트를 읽기 중심으로 보는 route다.
- read mode는 write mode에서 명시적 전환으로 들어갈 수 있어야 한다.
- 진입 맥락은 analytics/navigation layer에서 처리하고 canonical URL에는 `video_id`와 mode만 남긴다.

## Navigation Paths

### Happy Path

1. `/feed` 진입
2. source가 없으면 `/sources`로 이동해 채널 등록
3. `/feed`로 돌아와 최신 영상 목록 탐색
4. 영상 선택
5. `/videos/[video_id]/write` 진입
6. 노트 작성과 타임스탬프 상호작용 수행

### Escape Hatch

1. `/feed` 진입
2. "영상 URL로 바로 열기" 입력 surface에 URL 붙여넣기
3. 명시적 `열기` action 수행
4. `/videos/[video_id]/write` 진입

### Review Path

1. `/videos/[video_id]/write` 또는 direct link 진입
2. 명시적 mode switch로 `/videos/[video_id]/read` 전환
3. 노트 읽기와 timestamp click seek 수행

### Revisit Path

1. `/notes` 진입
2. 최근 수정한 note가 있는 영상 목록 확인
3. 항목 선택
4. `/videos/[video_id]/read` 진입

## Screen Boundary Notes

- `Source 등록`과 `Video Feed`는 분리된 화면으로 유지한다.
- `Video Feed`는 탐색 중심 화면이고, source가 없는 경우에만 source 등록 CTA를 강하게 드러낸다.
- `Note List`는 탐색이 아니라 재진입 중심 화면이다.
- `Note List`의 제목/썸네일은 enrichment이고, row 존재 여부는 local note 정본이 결정한다.
- video workspace는 별도 modal이 아니라 독립 route family다.
- `Video Write`와 `Video Read`는 같은 `video_id`와 note SoT를 공유하는 sibling route다.
- timestamp 삽입은 `write` route의 interaction이고, timestamp click seek은 `read` route의 interaction이다.

## Out of Scope

- 인증 기반 온보딩 route
- 별도 검색 화면
- 최근 본 영상 전용 화면
- playlist source 전용 화면
- settings/프로필 화면
