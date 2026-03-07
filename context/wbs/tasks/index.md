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

| slice_id | goal | planning_status | planned_flow | workspaces | run_id | 메모 |
|---|---|---|---|---|---|---|
| [MVP-SOURCE-ADD-CHANNEL](./MVP-SOURCE-ADD-CHANNEL.yaml) | 학습 채널 URL을 등록할 수 있다 | ready_for_flow | - | 구현: `feat/mvp-source-add-channel`, 버그 수정: `fix/mvp-source-add-channel-validation` | - | 다중 workspace 예시가 포함된 slice |
| [MVP-TS-INSERT](./MVP-TS-INSERT.yaml) | 현재 재생 시점을 노트에 삽입할 수 있다 | planned | - | - | - | 타임스탬프 형식과 이벤트 책임이 아직 미확정 |
| [MVP-TIMESTAMP-CLICK-SEEK](./MVP-TIMESTAMP-CLICK-SEEK.yaml) | 노트 타임스탬프 클릭으로 플레이어 seek이 가능하다 | planning_blocked | - | 구현: `feat/mvp-timestamp-click-seek` | - | 형식 contract와 seek 표면이 미확정 |
| [MVP-VIDEO-OPEN-BY-URL](./MVP-VIDEO-OPEN-BY-URL.yaml) | 영상 URL로 Player + Note 화면에 바로 진입할 수 있다 | draft | - | - | - | URL 패턴 범위를 먼저 좁혀야 함 |
