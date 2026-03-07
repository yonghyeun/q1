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

| slice_id | goal | planning_status | planned_flow | branch | worktree | run_id | 메모 |
|---|---|---|---|---|---|---|---|
| [MVP-TS-INSERT](./MVP-TS-INSERT.yaml) | 현재 재생 시점을 노트에 삽입할 수 있다 | planned | - | - | - | - | 타임스탬프 형식과 이벤트 책임이 아직 미확정 |
