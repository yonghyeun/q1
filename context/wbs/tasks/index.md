# WBS Task Index

이 문서는 `context/wbs/tasks/*.yaml`의 요약 projection이다.
정본은 개별 task YAML이며, 이 문서는 backlog 전체를 빠르게 읽기 위한 overview다.

## 상태 해석

- `draft`: 초안 단계
- `planned`: 기본 필드가 채워졌지만 flow 준비 전
- `planning_blocked`: planning 단계에서 막힘
- `ready_for_flow`: planned flow 작성 가능
- `ready_for_dispatch`: flow와 binding이 준비돼 dispatch 직전
- `archived`: 더 이상 다루지 않음
- `cancelled`: scope에서 제외됨

## Task Summary

정확한 branch/worktree path는 각 task YAML이 정본이며,
이 표는 workspace 요약만 보여준다.

<!-- wbs-task-summary:start -->
| slice_id | goal | planning_status | planned_flow | workspaces | run_id |
|---|---|---|---|---|---|
| [MVP-NOTE-LIST-BY-UPDATED-AT](./MVP-NOTE-LIST-BY-UPDATED-AT.yaml) | 사용자가 작성한 노트가 있는 영상을 `updated_at` 기준 목록으로 볼 수 있다. | ready_for_flow | - | - | - |
| [MVP-NOTE-LIST-METADATA-ENRICHMENT](./MVP-NOTE-LIST-METADATA-ENRICHMENT.yaml) | 사용자가 Note List에서 영상 제목과 썸네일을 우선 보고 항목을 빠르게 식별할 수 있다. | planned | - | - | - |
| [MVP-NOTE-LOCAL-PERSISTENCE](./MVP-NOTE-LOCAL-PERSISTENCE.yaml) | 사용자가 영상별 노트를 작성하고 브라우저 로컬 저장으로 다시 이어서 편집할 수 있다. | planned | - | - | - |
| [MVP-PLAYER-NOTE-WORKSPACE](./MVP-PLAYER-NOTE-WORKSPACE.yaml) | 사용자가 선택한 영상의 플레이어와 노트를 같은 작업 공간에서 write/read 모드로 사용할 수 있다. | ready_for_flow | - | - | - |
| [MVP-SOURCE-ADD-CHANNEL](./MVP-SOURCE-ADD-CHANNEL.yaml) | 사용자가 학습할 채널 URL을 등록해 소스 목록에 추가할 수 있다. | ready_for_flow | - | 구현: `feat/mvp-source-add-channel`, 버그 수정: `fix/mvp-source-add-channel-validation` | - |
| [MVP-TIMESTAMP-CLICK-SEEK](./MVP-TIMESTAMP-CLICK-SEEK.yaml) | 사용자가 Video Read 화면의 타임스탬프를 클릭하면 현재 플레이어가 해당 시점으로 이동한다. | planning_blocked | - | 구현: `feat/mvp-timestamp-click-seek` | - |
| [MVP-TS-INSERT](./MVP-TS-INSERT.yaml) | 사용자가 Video Write 화면에서 현재 재생 시점을 노트에 삽입할 수 있다. | planned | - | - | - |
| [MVP-VIDEO-FEED-CHANNEL-FILTER](./MVP-VIDEO-FEED-CHANNEL-FILTER.yaml) | 사용자가 영상 피드 범위를 `All` 또는 특정 채널 1개로 좁힐 수 있다. | ready_for_flow | - | - | - |
| [MVP-VIDEO-FEED-LATEST-LIST](./MVP-VIDEO-FEED-LATEST-LIST.yaml) | 사용자가 등록한 채널들의 최신 영상을 앱 내부 피드에서 기본 목록으로 볼 수 있다. | ready_for_flow | - | - | - |
| [MVP-VIDEO-FEED-LOAD-OLDER](./MVP-VIDEO-FEED-LOAD-OLDER.yaml) | 사용자가 현재 선택한 피드 범위 기준으로 더 오래된 영상을 추가로 불러올 수 있다. | draft | - | - | - |
| [MVP-VIDEO-OPEN-BY-URL](./MVP-VIDEO-OPEN-BY-URL.yaml) | 사용자가 유튜브 영상 URL을 붙여넣어 Video Write 화면으로 바로 진입할 수 있다. | ready_for_flow | - | - | - |
| [MVP-VIDEO-OPEN-FROM-FEED](./MVP-VIDEO-OPEN-FROM-FEED.yaml) | 사용자가 피드에서 선택한 영상을 Video Write 화면으로 열 수 있다. | ready_for_flow | - | - | - |
| [MVP-VIDEO-OPEN-FROM-NOTE-LIST](./MVP-VIDEO-OPEN-FROM-NOTE-LIST.yaml) | 사용자가 Note List에서 선택한 영상을 Video Read 화면으로 열 수 있다. | ready_for_flow | - | - | - |
<!-- wbs-task-summary:end -->
