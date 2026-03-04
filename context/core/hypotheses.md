# Hypotheses (MVP)

이 제품의 "현재" 가설을 관리한다.

Terminology SoT: [`docs/product/glossary.md`](../../docs/product/glossary.md)

- 가설은 측정 가능하게 쓴다.
- 가설 수는 적을수록 좋다(상위 5개를 넘기지 않는다).
- 실험 1개는 가설 1개를 검증한다.

## Hypothesis List

| ID | Hypothesis | Primary Metric | Success Bar | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| H1 | 첫 세션에서 타임스탬프 삽입(단축키/버튼)을 제공하면 Activation이 증가한다. | `timestamp_inserted / new_users` | TBD | backlog | 코어 가치 행동 |
| H2 | 타임스탬프가 클릭 시 해당 시점으로 점프하면 D7 Retention이 증가한다. | D7 retention | TBD | backlog | "다시 찾기" 강화 |
| H3 | Video URL Open을 제공하면 time-to-first-note가 줄고 Activation이 증가한다. | time-to-first-note | TBD | backlog | 진입 마찰 제거 |
| H4 | Video Feed에서 `Load older`를 제공하면 학습 세션에서의 영상 열람/노트 작성이 증가한다. | `note_created / active_users` | TBD | backlog | 과거 영상 접근(학습 백로그) |

## 운영 규칙

- 각 가설의 `Success Bar`(기준치)는 배포 전에 채운다.
- `Status`는 `backlog | active | validated | rejected` 정도면 충분하다.
