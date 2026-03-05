# Metrics (MVP)

MVP 단계에서 보는 지표 정의.

목표: "가설 검증/실험"을 위한 최소 공통 언어를 만든다. 완벽함보다 일관성이 중요하다.

## North Star (Core Value)

- `timestamped_note_created`
  - 의미: 유저가 영상에서 지식을 추출해서, 근거(타임스탬프)와 함께 기록으로 남겼다.

## Activation (초기 가치 도달)

- 정의(권장): "신규 유저가 첫 세션에서 `timestamp_inserted`를 1회 이상 수행한 비율"
- 보조 지표(선택)
  - `note_created` 비율
  - `source_added` 후 `video_opened`까지의 전환률

## Retention (재방문/재사용)

- D1 retention: 가입(또는 첫 방문) 후 1일 내 재방문 비율
- D7 retention: 가입(또는 첫 방문) 후 7일 내 재방문 비율

## Quality / Guardrails (망가지면 안 되는 것)

- 클라이언트 에러율(예: 5xx/JS error)
- p95 페이지 로딩(대략적인 체감 지표로 충분)
- 코어 플로우 이탈(온보딩에서 막히는지)

## Note

- MVP에서는 "정답 지표"가 아니라 "같은 정의로 반복 측정"이 목표다.
- 숫자는 `context/experiments/*`에서 실험 단위로 기록한다.

