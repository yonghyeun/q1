# MVP Spec (Outline)

기능 목록이 아니라 "경험/플로우" 기준으로 적는다.

## Core Flow (Happy Path)

1. 유저가 채널 URL을 등록한다.
2. 등록한 채널들의 최신 영상 피드(기본값 30개, 기본 필터: All)에서 하나를 선택한다.
3. 영상이 임베드 플레이어로 재생된다(다운로드 없음).
4. 같은 화면에서 비디오당 1개의 마크다운 노트를 작성/열람/수정한다(자동저장).
5. 단축키/버튼으로 현재 시점 타임스탬프를 노트에 삽입한다.
6. 나중에 타임스탬프를 클릭하면 플레이어가 해당 시점으로 점프(seek)한다.

## Core Flow (Escape Hatch)

- 유저가 유튜브 "영상 URL"을 붙여넣는다.
- 해당 영상의 Player + Note 화면으로 바로 진입한다(노트는 `video_id` 기준으로 저장/재호출).

## Screens (최소)

- Source 등록 화면
- Video 목록 화면
- Player + Note 편집 화면(핵심)

## Video Feed & Pagination

목록은 "학습 세션 보호(산만함 최소화)"를 위해 유튜브 홈/추천 대신, 앱 내부에서만 탐색한다.

- 기본값: 최신 30개 표시
- 필터: `All`(기본) 또는 특정 채널 1개(단일 선택)
- `Load older`: 현재 선택된 필터 기준으로 30개씩 추가 로딩
  - `All`의 경우: "채널별로 가져온 버퍼"를 `publishedAt` 기준으로 머지(k-way merge)해 가상 페이지네이션을 만든다.
  - 효율 원칙: `Load older` 시 매번 모든 채널을 추가 호출하지 않고, "필요한 채널"만 추가 fetch 한다(버퍼가 부족한 채널부터).

## Keyboard Shortcuts (초기)

- 현재 타임스탬프 삽입
- 재생/일시정지 토글
- 타임스탬프 삽입 + 자동 일시정지
- 10초 뒤로 이동 / 10초 앞으로 이동

## Persistence (MVP)

- 회원가입/로그인 없이 사용한다.
- 노트/설정은 브라우저 로컬 저장소(LocalStorage)에 저장한다.
- 클라우드 동기화/백업이 없고, 브라우저 데이터 삭제 시 유실될 수 있다.

## Timestamp Format

- 노트에는 마크다운 링크 형태로 남긴다.
  - 예: `- [00:12:34](https://www.youtube.com/watch?v=VIDEO_ID&t=754s)`
- 앱에서 클릭 시 외부 이동이 아니라, 플레이어 `seek`으로 동작한다.

## Data Model (초기 스케치)

- `Source`: channel
- `Video`: youtube video id + metadata
- `VideoOpen`: `video_id` + `open_method` (`feed|url`) + `opened_at` (선택: 최근 열어본 영상)
- `Note`: video_id + markdown (+ updated_at)
- `Marker`: note_id + timestamp_seconds (+ optional text)

## Analytics (필수 이벤트)

- 이벤트 정의는 `context/analytics/events.md`를 따른다.

## Out of Scope

- 영상 다운로드/클리핑
- 회원가입/로그인, 클라우드 동기화/백업
- 고급 협업(권한/코멘트)
- 정교한 추천/개인화 피드
- 플레이리스트 URL/ID 소스 등록(채널만 지원)

## Future (Post-MVP, Important)

- 작성 중인 텍스트에 암묵적으로 타임스탬프를 저장한다(영상 재생 상태에서 입력되는 문단/라인 단위로 앵커링).
- Read 모드에서 영상 시간이 변하면(재생/seek) 해당 타임스탬프 구간의 텍스트를 강조/밑줄 처리하거나, 스크롤을 동기화한다.
- 플레이리스트 URL/ID를 소스로 등록해 코스/시리즈 단위 학습을 지원한다(이번 사이클엔 구현하지 않음).

## Release Plan (MVP)

- 배포 단위는 "실험 1개"를 원칙으로 한다(`context/core/deploy-first.md`).
