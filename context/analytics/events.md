# Analytics Events (MVP)

배포-검증 루프를 돌리기 위한 최소 이벤트 사전.

Terminology SoT: [`docs/product/glossary.md`](../../docs/product/glossary.md)

## 원칙

- 이벤트 이름은 `snake_case`로 통일한다.
- 코어 플로우에서 "무조건 필요"한 이벤트만 먼저 정의한다.
- 개인정보/민감정보는 이벤트로 보내지 않는다.

## 공통 프로퍼티(권장)

- `user_id` (익명/로컬 식별자. 로그인 없음, LocalStorage 기반)
- `session_id`
- `client_ts` (클라이언트 타임스탬프)
- `app_version`

## 이벤트 목록 (최소)

- `source_added`
  - 언제: ChannelSource(채널 URL)를 등록했을 때
  - props: `source_type` (`channel`), `source_id`(가능하면), `source_url`

- `video_opened`
  - 언제: 유저가 특정 영상을 열고 재생 화면에 진입했을 때
  - props: `video_id`, `open_method` (`feed|url`), `source_id`(선택), `feed_filter` (`all|channel`), `filter_source_id`(선택)

- `video_feed_load_older_clicked`
  - 언제: Video Feed에서 `Load older`를 클릭했을 때
  - props: `feed_filter` (`all|channel`), `filter_source_id`(선택), `page_size`(기본 30)

- `note_created`
  - 언제: 노트(문서)가 처음 생성됐을 때
  - props: `note_id`, `video_id`

- `timestamp_inserted`
  - 언제: 노트에 타임스탬프가 삽입됐을 때(단축키/버튼 포함)
  - props: `note_id`, `video_id`, `timestamp_seconds`, `method` (`hotkey|button|auto`)

- `timestamp_clicked`
  - 언제: 노트의 타임스탬프 링크를 클릭해 해당 시점으로 점프했을 때
  - props: `note_id`, `video_id`, `timestamp_seconds`

- `search_used` (선택)
  - 언제: 검색을 실행했을 때
  - props: `scope` (`notes|videos`), `query_len`

## MVP 범위 밖(예시)

- 상세 퍼널/코호트 자동 리포트
- 복잡한 A/B 테스트 프레임워크(필요해지면 도입)
- PlaylistSource(플레이리스트) 기반 이벤트(후속 MVP)
