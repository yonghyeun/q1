# API Behavior Spec (MVP)

이 문서는 `docs/product/contracts/api-youtube.ts`의 integration contract 위에서,
`unote` MVP가 실제로 어떤 성공/실패 의미를 제품적으로 해석하는지 고정한다.

목표:

- 화면이 integration 오류를 일관되게 해석하게 한다.
- YouTube 메타데이터를 note 정본과 분리해 best-effort enrichment로 다루게 한다.
- URL open, source 등록, feed hydrate에서 partial/degraded 기준을 흔들리지 않게 만든다.

관련 SoT:

- [MVP spec](mvp-spec.md)
- [Sitemap](sitemap.md)
- [Screen spec](screen-spec.md)
- [Frontend routing/state](frontend-routing-and-state.md)
- [YouTube integration contract](contracts/api-youtube.ts)
- [Storage contracts](contracts/storage.ts)
- [YouTube 정책 체크](youtube-api-policy-notes.md)

## 원칙

- integration boundary는 YouTube 원본 응답을 그대로 노출하지 않고, UI가 바로 쓸 수 있는 의미로 정규화한다.
- `notes_by_video_id`와 source 목록은 앱의 정본이다. YouTube 메타데이터는 enrichment다.
- metadata hydrate 실패가 note 접근이나 route 진입을 막으면 안 된다.
- UI 분기는 `message`가 아니라 `error.code` 기준으로 한다.
- `All` 피드의 partial success는 단일 integration call의 책임이 아니라, 여러 채널 호출을 합성하는 앱 레이어 책임이다.

## 공통 응답 의미

### 성공

- `ok: true`는 해당 route의 코어 목적을 만족하는 최소 데이터가 준비됐다는 뜻이다.
- 부가 필드가 빠질 수 있는 경우에도, 코어 목적이 성립하면 성공으로 본다.

예:

- `parse-video-url`은 `video_id`를 얻으면 성공이다.
- `get-videos-by-id`는 일부 `video_id`만 찾았어도 성공일 수 있다.

### 실패

- `ok: false`는 현재 route의 코어 목적이 성립하지 않았다는 뜻이다.
- 실패 응답은 retry, fallback, inline error copy의 기준으로만 쓰고, 원본 upstream 상세를 UI에 직접 노출하지 않는다.

## Error Code Baseline

MVP에서 UI가 안정적으로 분기해야 하는 error code는 아래 범위로 제한한다.

| Code | 의미 | UI 기본 반응 |
|---|---|---|
| `bad_request` | 필수 입력 누락, 형식 오류 | 인라인 입력 오류 |
| `unsupported_url_pattern` | MVP에서 허용하지 않는 YouTube URL 패턴 | 인라인 입력 오류 |
| `not_found` | 대상 채널/영상을 해석하지 못함 | 입력 오류 또는 비치명 경고 |
| `duplicate_source` | 이미 등록된 채널 source | 중복 안내, 저장 안 함 |
| `upstream_unavailable` | YouTube API 또는 네트워크 문제로 현재 요청 수행 불가 | retry 가능 오류 |
| `quota_exceeded` | YouTube quota 또는 운영 제한으로 처리 불가 | 비치명 경고 + 나중에 재시도 유도 |

`invalid_video_id`, `invalid_channel_url`처럼 더 세분화된 내부 오류는 운영 로그에서 쓸 수 있지만,
MVP UI contract는 위 baseline만 전제로 한다.

## Integration Action Rules

### 1. `resolve channel`

목적:

- 사용자가 입력한 channel URL을 canonical `channel_id`로 정규화한다.
- source 등록 전에 URL이 지원 범위 안인지 판정한다.

MVP 지원 URL 패턴:

- `https://www.youtube.com/channel/{channel_id}`
- `https://youtube.com/channel/{channel_id}`
- `https://www.youtube.com/@handle`
- `https://youtube.com/@handle`

MVP 비지원 패턴:

- `/c/...`
- `/user/...`
- playlist URL
- video URL

성공 기준:

- `channel_id`를 결정할 수 있으면 성공이다.
- `channel` 메타데이터와 `canonical_channel_url`은 있으면 함께 주되, source 생성의 필수값은 `channel_id`다.

실패 기준:

- URL 형식이 채널 URL이 아니거나 MVP 비지원 패턴이면 `unsupported_url_pattern`
- 형식은 맞지만 채널을 찾지 못하면 `not_found`
- 이미 등록된 channel_id라면 앱 또는 integration layer에서 `duplicate_source`
- upstream 조회 자체가 불가능하면 `upstream_unavailable`

화면 연결:

- `/sources`는 `duplicate_source`를 실패가 아닌 사용성 안내로 처리한다.
- 성공 시 source 저장은 앱 레이어가 담당한다.

### 2. `list channel videos`

목적:

- 특정 `channel_id` 기준 최신 영상 목록 한 페이지를 가져온다.

성공 기준:

- 요청한 채널 하나에 대한 `items`를 반환하면 성공이다.
- `items`는 `published_at` 정렬이 가능해야 하며, 피드 row 렌더에 필요한 최소 메타데이터를 포함한다.
- `items.length === 0`도 정상 성공이다.

실패 기준:

- `channel_id` 누락/형식 오류는 `bad_request`
- 채널을 해석할 수 없으면 `not_found`
- upstream 실패나 quota 문제는 `upstream_unavailable` 또는 `quota_exceeded`

앱 레이어 합성 규칙:

- `All` 피드는 등록된 source별로 이 endpoint를 호출한 뒤 머지한다.
- 여러 채널 중 하나 이상 성공하면 `/feed`는 partial/degraded success로 본다.
- 모든 채널 호출이 실패하면 `/feed`는 초기 오류 상태로 본다.
- 일부 채널 실패는 banner 또는 비치명 경고로만 드러내고, 성공한 채널의 row는 그대로 보여 준다.

### 3. `get videos by id`

목적:

- video metadata를 batch hydrate한다.
- note list와 video workspace의 title/thumbnail enrichment에 사용한다.

성공 기준:

- 요청한 `video_ids` 중 조회 가능한 항목을 `items`에 담아 반환하면 성공이다.
- 일부 `video_id`가 빠져 있어도 전체 요청을 실패로 보지 않는다.

실패 기준:

- `video_ids` 누락, 빈 배열, 형식 오류는 `bad_request`
- upstream 전체 호출 실패는 `upstream_unavailable`
- quota 제한은 `quota_exceeded`

누락된 `video_id` 해석:

- private/deleted/unavailable
- 일시적 upstream 누락
- 아직 hydrate하지 못한 상태

UI 규칙:

- `/notes`와 `/videos/[video_id]/*`는 누락된 metadata를 degraded 상태로 취급한다.
- fallback title, placeholder thumbnail, `video_id` 기반 식별은 계속 유지한다.
- metadata 누락만으로 note row나 video route 진입을 막지 않는다.

### 4. `parse video url`

목적:

- 유저가 붙여넣은 video URL을 `(video_id, t_seconds)`로 정규화한다.

MVP 지원 URL 패턴:

- `https://www.youtube.com/watch?v={video_id}`
- `https://youtube.com/watch?v={video_id}`
- `https://m.youtube.com/watch?v={video_id}`
- `https://youtu.be/{video_id}`

추가 허용:

- `t` query parameter는 있으면 초 단위로 파싱한다.
- `list`, `feature`, `si` 같은 부가 query는 무시한다.

MVP 비지원 패턴:

- channel URL
- playlist 단독 URL
- `shorts/...`
- `live/...`

성공 기준:

- `video_id`를 추출할 수 있으면 성공이다.
- `published_at`은 optional enrichment다.
- metadata 조회가 실패해도 parse 성공은 유지한다.

실패 기준:

- URL 형식 오류는 `bad_request`
- MVP 비지원 패턴은 `unsupported_url_pattern`
- video_id를 찾지 못하면 `not_found`
- upstream 메타데이터 조회 실패는 parse 실패로 승격하지 않는다.

화면 연결:

- `/feed`의 "영상 URL로 바로 열기"는 parse 성공 시 `/videos/[video_id]/write`로 이동한다.
- 이미 note가 있어도 route는 항상 `write`로 들어간다.

## Metadata Hydration Rules

- title/thumbnail/channel metadata는 모두 best-effort enrichment다.
- 앱은 metadata를 LocalStorage에 캐시할 수 있지만, note/source보다 약한 저장소로 취급한다.
- 캐시 miss 또는 stale은 API 재조회 트리거일 뿐, route 실패 사유가 아니다.
- hydrate 실패 시 UI는 placeholder와 비치명 경고로 남고, 핵심 행동은 유지한다.

## Screen-Specific Fallback

### `/sources`

- `unsupported_url_pattern`, `not_found`, `duplicate_source`는 모두 인라인 입력 오류/안내다.
- source 목록은 유지된다.

### `/feed`

- source가 없으면 empty state가 우선이다.
- source가 있고 일부 채널 호출만 실패하면 degraded banner와 함께 성공한 row를 보여 준다.
- URL parse 실패는 feed list와 분리된 입력 surface 오류로 처리한다.

### `/notes`

- note row의 존재 여부는 `notes_by_video_id`가 결정한다.
- metadata hydrate 실패는 row를 제거하지 않는다.

### `/videos/[video_id]/write` / `/read`

- metadata hydrate 실패는 컨텍스트 바 degraded 상태로만 반영한다.
- 플레이어 초기화 자체가 불가능한 경우에만 workspace 오류 상태로 승격한다.

## MVP Non-Goals

- YouTube 원본 에러 코드 전부를 1:1로 노출
- metadata 최신성의 강한 보장
- playlist, shorts, live URL까지 모두 지원
- batch API partial warning 필드를 별도 설계

## Implementation Note

- 이 문서는 route path 자체를 고정하지 않는다.
- 실제 구현은 `Next.js route handler`, `server action`, 별도 proxy/BFF 중 무엇이든 될 수 있다.
- MVP 현재 판단은 API key 보호를 위해 얇은 서버 측 proxy가 유력하지만,
  product contract는 그 구현 선택보다 오래 유지되는 문서로 본다.
- 현재 프로젝트의 기본 구현 바인딩은 `apps/web` 내부 Next.js route handler와
  `/api/youtube/*` route family를 우선 가정한다.

## WBS Alignment Notes

- `MVP-VIDEO-OPEN-BY-URL`의 URL 지원 범위는 이 문서의 `parse-video-url` 규칙으로 고정한다.
- `MVP-VIDEO-FEED-LATEST-LIST`의 partial failure 기준은 이 문서의 `list-channel-videos` 합성 규칙으로 고정한다.
- note list metadata enrichment는 cache miss보다 fallback 유지 여부를 더 중요한 acceptance로 본다.
