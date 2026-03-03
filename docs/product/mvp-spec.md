# MVP Spec (Outline)

기능 목록이 아니라 "경험/플로우" 기준으로 적는다.

## Core Flow (Happy Path)

1. 유저가 채널/플레이리스트 URL을 등록한다.
2. 영상 목록에서 하나를 선택한다.
3. 영상이 임베드 플레이어로 재생된다.
4. 같은 화면에서 마크다운 노트를 작성한다.
5. 단축키/버튼으로 현재 시점 타임스탬프를 삽입한다.
6. 나중에 타임스탬프를 클릭하면 해당 시점으로 점프한다.

## Screens (최소)

- Source 등록 화면
- Video 목록 화면
- Player + Note 편집 화면(핵심)

## Keyboard Shortcuts (초기)

- (예: 현재 타임스탬프 삽입)
- (예: 재생/일시정지 토글)

## Data Model (초기 스케치)

- `Source`: channel|playlist|video
- `Video`: youtube video id + metadata
- `Note`: video_id + markdown
- `Marker`: note_id + timestamp_seconds (+ optional text)

## Analytics (필수 이벤트)

- 이벤트 정의는 `context/analytics/events.md`를 따른다.

## Out of Scope

- 영상 다운로드/클리핑
- 고급 협업(권한/코멘트)
- 정교한 추천/개인화 피드

## Release Plan (MVP)

- 배포 단위는 "실험 1개"를 원칙으로 한다(`context/core/deploy-first.md`).

