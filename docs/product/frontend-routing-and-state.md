# Frontend Routing And State (MVP)

이 문서는 `unote` MVP의 프런트엔드 라우팅과 상태 소유권을 고정한다.
목표는 route param, LocalStorage 정본, 화면 내부 transient state를 섞지 않고
각 화면이 어떤 입력으로 복원되는지 명확하게 만드는 것이다.

관련 SoT:
- [MVP spec](mvp-spec.md)
- [Sitemap](sitemap.md)
- [Screen spec](screen-spec.md)
- [Domain contracts](contracts/domain.ts)
- [Storage contracts](contracts/storage.ts)

## 원칙

- canonical entity route는 `video_id`만 소유한다.
- 화면 진입을 결정하는 식별자와, 화면 안에서 복원 가능한 UI 상태를 구분한다.
- LocalStorage의 정본은 유저 생성 데이터와 최소 UI 복원 상태에만 사용한다.
- YouTube 메타데이터는 route 진입을 결정하지 않는다.
- metadata hydrate 실패는 degraded UI로 처리하고 route 전환이나 note 접근을 막지 않는다.

## State Layers

### 1. Route State

URL로 공유되거나 새로고침 후에도 동일하게 해석되어야 하는 상태다.

- `/`
- `/sources`
- `/feed`
- `/notes`
- `/videos/[video_id]`
- `/videos/[video_id]/write`
- `/videos/[video_id]/read`

MVP에서 route가 소유하는 값:

- `video_id`
- `mode` (`write|read`, path segment로 표현)

MVP에서 route가 소유하지 않는 값:

- `feed_filter`
- `filter_source_id`
- `open_method`
- note list의 metadata hydrate 상태
- 플레이어 초기화 pending 여부
- note autosave pending 여부

### 2. Local Persistent State

새로고침이나 재방문 후 복원될 수 있는 앱 내부 정본이다.

- `sources`
- `notes_by_video_id`
- `video_opens`
- `ui_state`
- `caches`

`ui_state`에 포함되는 MVP 필드:

- `feed_filter`
- `filter_source_id`
- `last_opened_video_id`

현재 제품 계약 기준:

- `feed_filter`와 `filter_source_id` 필드는 storage schema에는 존재하지만,
  fresh entry 기본값을 덮는 복원 규칙으로는 아직 사용하지 않는다.
- `last_opened_video_id`는 최근 진입 참고값으로만 사용 가능하다.

### 3. Session / Transient UI State

현재 렌더 사이클이나 화면 수명 동안만 의미가 있는 상태다.

- 입력 필드 draft
- loading / hydrating / degraded banner 표시 여부
- `Load older` pending
- note autosave pending
- 현재 화면에서만 보이는 validation error
- metadata placeholder 노출 여부

## Route Ownership

### `/`

- 책임: 첫 진입 redirect
- canonical state: 없음
- 복원 규칙: 즉시 `/feed`로 이동

### `/sources`

- 책임: source 등록과 등록 목록 확인
- canonical state: 없음
- LocalStorage 읽기: `sources`
- transient state:
  - 채널 URL input draft
  - validation pending
  - duplicate / invalid error

### `/feed`

- 책임: 영상 탐색과 `write` 진입
- canonical state: route 자체만
- LocalStorage 읽기:
  - `sources`
  - `caches.channels_by_id`
  - `caches.videos_by_id`
- LocalStorage 쓰기:
  - 선택적으로 `video_opens`
- transient state:
  - initial loading
  - partial/degraded warning
  - URL open input draft
  - `Load older` pending
  - merged feed rows

`/feed` 진입 기본값:

- 항상 `All`
- `filter_source_id`는 현재 세션에서 `feed_filter=channel`일 때만 의미가 있다.

### `/notes`

- 책임: 저장된 note 목록에서 재진입 시작
- canonical state: route 자체만
- LocalStorage 읽기:
  - `notes_by_video_id`
  - `caches.videos_by_id`
- LocalStorage 쓰기:
  - 선택적으로 `video_opens`
- transient state:
  - note rows derived from `notes_by_video_id`
  - metadata hydrating
  - metadata degraded banner

`/notes` 정렬 원칙:

- row 정렬의 정본은 `note.updated_at`
- metadata는 row 표시만 enrich 하고 정렬 기준을 바꾸지 않는다.

### `/videos/[video_id]`

- 책임: canonical entry route
- canonical state:
  - `video_id`
- 동작:
  - 즉시 `/videos/[video_id]/write`로 redirect

### `/videos/[video_id]/write`

- 책임: 편집 중심 video workspace
- canonical state:
  - `video_id`
  - `mode=write`
- LocalStorage 읽기:
  - `notes_by_video_id[video_id]`
  - `caches.videos_by_id[video_id]`
  - `ui_state.last_opened_video_id`
- LocalStorage 쓰기:
  - `notes_by_video_id[video_id]`
  - `ui_state.last_opened_video_id`
  - 선택적으로 `video_opens`
- transient state:
  - player initializing
  - autosave pending/degraded
  - editor draft buffer
  - timestamp insertion feedback

### `/videos/[video_id]/read`

- 책임: 읽기 중심 video workspace
- canonical state:
  - `video_id`
  - `mode=read`
- LocalStorage 읽기:
  - `notes_by_video_id[video_id]`
  - `caches.videos_by_id[video_id]`
  - `ui_state.last_opened_video_id`
- LocalStorage 쓰기:
  - `ui_state.last_opened_video_id`
  - 선택적으로 `video_opens`
- transient state:
  - player initializing
  - renderer degraded
  - timestamp binding pending

## Navigation Context

`open_method`, `feed_filter`, `filter_source_id`, `source_id`는 navigation/analytics context다.
이 값들은 canonical URL에 넣지 않고, 화면 전환 시 이벤트 또는 in-memory transition data로만 전달한다.

기본 규칙:

- `feed -> write`
  - `open_method=feed`
  - 현재 `feed_filter`, `filter_source_id`를 함께 전달할 수 있다.
- `url open -> write`
  - `open_method=url`
  - feed context는 없다.
- `notes -> read`
  - `open_method=note_list`
  - feed context는 없다.

이 맥락은 새로고침 후 복원 대상이 아니다.
새로고침 이후에도 해석 가능한 상태는 `video_id`와 route mode뿐이다.

## Persistence Ownership

### `notes_by_video_id`

- 정본
- keyed by `video_id`
- write/read가 동일 note record를 공유한다.
- note list row는 여기서 파생한다.

### `ui_state`

- 복원 보조 상태
- 정본 entity 데이터가 아니다.
- MVP 필드:
- `feed_filter`
- `filter_source_id`
- `last_opened_video_id`

운영 규칙:

- `feed_filter`와 `filter_source_id`는 storage schema에 존재하지만, 현재 MVP에서는 fresh entry 복원 규칙으로 사용하지 않는다.
- `last_opened_video_id`는 `write` 또는 `read` 진입 시 갱신할 수 있다.
- `/notes`의 정렬이나 선택 상태는 `ui_state`에 저장하지 않는다.

### `video_opens`

- 분석/최근 열기 성격의 선택 저장소
- note 정본이나 route 복원의 필수 입력이 아니다.
- 비어 있어도 코어 흐름은 성립해야 한다.

### `caches`

- title, thumbnail 같은 metadata의 보조 저장소
- route 진입 가능 여부를 결정하지 않는다.
- miss 또는 stale일 때 hydrate를 시도하고, 실패하면 degraded UI로 남긴다.

## Derived View Models

### Feed Rows

입력:

- `sources`
- fetched video summaries
- `feed_filter`
- `filter_source_id`
- optional cached metadata

출력:

- `/feed`에서 렌더링 가능한 row 목록

### Note List Rows

입력:

- `notes_by_video_id`
- optional `caches.videos_by_id`

출력 필드:

- `video_id`
- `updated_at`
- `title?`
- `thumbnail_url?`
- `is_metadata_degraded`

정렬:

- 항상 `updated_at desc`

## Degraded Behavior

### Feed

- 일부 채널 fetch 실패:
  - 전체 route는 유지
  - 가능한 row만 노출
  - 비치명 경고 노출

### Note List

- metadata miss 또는 hydrate 실패:
  - row 유지
  - fallback title 또는 `video_id` 노출
  - placeholder thumbnail 노출
  - `/videos/[video_id]/read` 진입은 유지

### Video Workspace

- metadata unavailable:
  - 플레이어와 note 정본은 가능한 범위에서 계속 연다
  - 제목/컨텍스트 바만 degraded 가능
- invalid/unavailable video:
  - player 영역 오류 표시
  - note 접근 정책은 후속 API behavior spec과 함께 구체화한다.

## Mode Switching Rules

- `write <-> read` 전환은 항상 같은 `video_id`를 유지한다.
- mode 전환은 route change지만 entity change는 아니다.
- note 정본을 다시 선택하지 않는다.
- 플레이어 재초기화 여부는 구현 세부지만, 사용자 맥락은 유지되는 것으로 본다.

## Defaults And Restoration

- root entry: `/feed`
- `/feed` default filter:
  - 항상 `All`
- `/notes` default view:
  - `notes_by_video_id` 기반 최신순 목록
- `/videos/[video_id]`:
  - 항상 `/write`로 보냄
- `last_opened_video_id`:
  - 최근 진입 편의를 위한 참고값일 뿐 자동 redirect 근거로 쓰지 않는다.

## Non-Goals

- query string 기반 deep state persistence
- server session 또는 auth session 도입
- 검색 query, 정렬 옵션, note list selection 복원
- player runtime state를 URL에 encode

## Open Follow-Ups

- `docs/product/api-behavior-spec.md`
  - unavailable/private video의 fetch/표시/열기 규칙
  - metadata hydrate 실패 시 API error mapping
- `docs/product/ui-conventions.md`
  - degraded, empty, loading 상태의 시각 규칙
  - list row와 workspace shell의 공통 UI 패턴
