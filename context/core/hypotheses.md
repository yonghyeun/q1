# Hypotheses (MVP)

이 제품의 "현재" 가설을 관리한다.

- 가설은 측정 가능하게 쓴다.
- 가설 수는 적을수록 좋다(상위 5개를 넘기지 않는다).
- 실험 1개는 가설 1개를 검증한다.

## Hypothesis List

| ID | Hypothesis | Primary Metric | Success Bar | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| H1 | 첫 세션에서 타임스탬프 삽입(단축키/버튼)을 제공하면 Activation이 증가한다. | `timestamp_inserted / new_users` | TBD | backlog | 코어 가치 행동 |
| H2 | 타임스탬프가 클릭 시 해당 시점으로 점프하면 D7 Retention이 증가한다. | D7 retention | TBD | backlog | "다시 찾기" 강화 |
| H3 | 채널 전체 수집보다 "학습 목록(선택한 영상만)"이 Activation을 증가시킨다. | Activation | TBD | backlog | 산만함/범위 제어 |
| H4 | 온보딩을 "플레이리스트(코스) URL 1개 입력"으로 단순화하면 첫 가치 도달 시간이 줄어든다. | time-to-first-note | TBD | backlog | 입력 마찰 제거 |

## 운영 규칙

- 각 가설의 `Success Bar`(기준치)는 배포 전에 채운다.
- `Status`는 `backlog | active | validated | rejected` 정도면 충분하다.

