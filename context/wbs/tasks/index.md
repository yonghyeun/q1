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
| [MVP-SOURCE-ADD-CHANNEL](./MVP-SOURCE-ADD-CHANNEL.yaml) | 사용자가 학습할 채널 URL을 등록해 소스 목록에 추가할 수 있다. | ready_for_flow | - | 구현: `feat/mvp-source-add-channel`, 버그 수정: `fix/mvp-source-add-channel-validation` | - |
| [MVP-TIMESTAMP-CLICK-SEEK](./MVP-TIMESTAMP-CLICK-SEEK.yaml) | 사용자가 노트 안의 타임스탬프를 클릭하면 현재 플레이어가 해당 시점으로 이동한다. | planning_blocked | - | 구현: `feat/mvp-timestamp-click-seek` | - |
| [MVP-TS-INSERT](./MVP-TS-INSERT.yaml) | 사용자가 Player + Note 화면에서 현재 재생 시점을 노트에 삽입할 수 있다. | planned | - | - | - |
| [MVP-VIDEO-OPEN-BY-URL](./MVP-VIDEO-OPEN-BY-URL.yaml) | 사용자가 유튜브 영상 URL을 붙여넣어 Player + Note 화면으로 바로 진입할 수 있다. | draft | - | - | - |
<!-- wbs-task-summary:end -->
