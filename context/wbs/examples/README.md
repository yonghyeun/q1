# WBS Example Artifacts

이 디렉터리는 packet / trace / run ledger가 실제로 어떻게 이어지는지 보여주는 예시를 저장한다.

현재 예시는 `timestamp-insert` 슬라이스 하나를 기준으로 구성한다.

- `handoff-packet.*.json`: operator가 actor에게 넘기는 실행 명세
- `trace-summary.*.json`: actor가 반환하는 실행 결과와 피드백
- `run-ledger.*.json`: operator가 현재 상태를 요약한 control-plane 상태

## 예시 읽는 순서

1. `timestamp-insert/handoff-packet.timestamp-insert.impl.v1.json`
2. `timestamp-insert/trace-summary.timestamp-insert.impl.v1.json`
3. `timestamp-insert/handoff-packet.timestamp-insert.impl.v2.json`
4. `timestamp-insert/trace-summary.timestamp-insert.impl.v2.json`
5. `timestamp-insert/run-ledger.timestamp-insert.review.json`

## 이 예시가 보여주는 것

### 1. 첫 handoff

- operator가 `EX-MVP-TS-INSERT` slice를 impl actor에게 전달한다.
- 첫 packet은 목표는 맞지만 editor command surface가 충분히 명시되지 않는다.

### 2. 첫 trace

- impl actor는 일부 구현과 unit test는 진행하지만 integration까지 닫지 못한다.
- trace는 `partial + orchestration`으로 결과를 반환하고, packet/contracts에 대한 feedback을 남긴다.

### 3. 두 번째 handoff

- operator는 실패를 "구현자 잘못"으로 처리하지 않고, packet 입력을 보강한 v2 packet을 다시 발행한다.
- 여기서 `editor-command-surface.md` 같은 보조 입력 문서를 handoff에 추가한다.

### 4. 두 번째 trace

- impl actor는 보강된 입력 기준으로 구현을 마무리하고 `success`를 반환한다.
- 다만 slice 전체 완료가 아니라, operator가 다음 integration handoff를 발행할 수 있는 수준까지 도달한 상태다.

### 5. run ledger

- ledger는 packet/trace를 덮어쓰지 않고 현재 상태만 요약한다.
- 이 예시에서는 `next_operator_decision: accept` 상태로, operator가 다음 packet을 발행할 준비가 된 시점을 보여준다.

## 중요한 해석 규칙

- `parent_wbs` 값은 실제 WBS가 아니라 예시용 식별자다.
- 이 디렉터리는 "형태"와 "흐름"을 보여주기 위한 것이지, 현재 저장소에 이미 해당 slice WBS가 존재한다는 뜻은 아니다.
- 실제 WBS를 만들기 시작하면 `parent_wbs`, `slice_id`, `owned_paths`를 실제 값으로 바꿔야 한다.

## 검증 방법

예시 JSON은 validator로 바로 검증할 수 있다.

```bash
python3 scripts/repo/validate_wbs_artifact.py \
  --kind handoff-packet \
  --file context/wbs/examples/timestamp-insert/handoff-packet.timestamp-insert.impl.v1.json
```

또는 테스트 전체를 실행한다.

```bash
python3 -m unittest scripts.repo.tests.test_validate_wbs_artifact \
  scripts.repo.tests.test_wbs_example_artifacts -v
```
