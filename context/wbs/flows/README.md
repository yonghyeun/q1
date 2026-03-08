# Planned Flow Artifacts

이 디렉터리는 slice별 `planned flow` 문서를 저장한다.

`planned flow`는 runtime run 안에서 생성되는 artifact가 아니라,
packet 발행 전에 준비되는 planning-layer artifact다.

## 파일 네이밍

- `<slice_id>.flow.vN.md`
- 예: `MVP-TS-INSERT.flow.v1.md`

권장 규칙:

- `slice_id`는 WBS와 동일한 식별자를 사용한다.
- `vN`은 route/node/loop 규칙이 실질적으로 바뀔 때만 올린다.
- 오탈자나 서술 보강 정도는 같은 버전에서 수정할 수 있다.
- runtime packet이 이미 발행된 뒤 경로 규칙이 바뀌면 기존 파일을 덮어쓰기보다 새 버전을 만든다.

## 운영 규칙

- 첫 packet은 자신이 따르는 planned flow 파일 경로를 `inputs`에 포함하는 것을 권장한다.
- 같은 slice에서 새 flow 버전이 발행되면 이후 packet은 새 버전 경로를 참조해야 한다.
- old packet은 old flow 버전을 그대로 가리키게 두어 audit/replay 가능성을 보존한다.
- flow 변경 사유는 operator decision 또는 별도 decision 문서에서 설명하는 것이 좋다.

## 현재 단계의 한계

현재 runtime schema는 `planned_flow_id`, `flow_version`, `node_id`를 필수 필드로 강제하지 않는다.
따라서 당장은 파일 경로 참조와 operator discipline으로 연결한다.
