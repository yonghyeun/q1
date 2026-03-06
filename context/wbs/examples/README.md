# WBS Example Artifacts

이 디렉터리는 packet / trace / operator decision / run ledger가 실제로 어떻게 이어지는지 보여주는 예시를 저장한다.

현재 예시는 `timestamp-insert` 슬라이스 하나를 기준으로 구성한다.

- `runs/<run_id>/packets/*.json`: operator가 actor에게 넘기는 실행 명세
- `runs/<run_id>/traces/*.json`: actor가 반환하는 실행 결과와 피드백
- `runs/<run_id>/decisions/*.json`: operator의 상태 전이와 판단 근거
- `runs/<run_id>/current.run-ledger.json`: 최신 control-plane 상태
- `runs/<run_id>/snapshots/*.run-ledger.json`: decision 직후 frozen projection

## 예시 읽는 순서

1. `runs/RUN-EX-2026-03-06-A/packets/0001.packet.EX-MVP-TS-INSERT.impl.json`
2. `runs/RUN-EX-2026-03-06-A/traces/0002.trace.H-EX-2026-03-06-001.impl.json`
3. `runs/RUN-EX-2026-03-06-A/decisions/0003.decision.EX-MVP-TS-INSERT.rework.json`
4. `runs/RUN-EX-2026-03-06-A/snapshots/0003.rework.run-ledger.json`
5. `runs/RUN-EX-2026-03-06-A/packets/0004.packet.EX-MVP-TS-INSERT.impl.json`
6. `runs/RUN-EX-2026-03-06-A/traces/0005.trace.H-EX-2026-03-06-002.impl.json`
7. `runs/RUN-EX-2026-03-06-A/decisions/0006.decision.EX-MVP-TS-INSERT.accept.json`
8. `runs/RUN-EX-2026-03-06-A/snapshots/0006.accept.run-ledger.json`
9. `runs/RUN-EX-2026-03-06-A/current.run-ledger.json`

## 이 예시가 보여주는 것

### 1. 첫 handoff

- operator가 `EX-MVP-TS-INSERT` slice를 impl actor에게 전달한다.
- 첫 packet은 목표는 맞지만 editor command surface가 충분히 명시되지 않는다.

### 2. 첫 trace

- impl actor는 일부 구현과 unit test는 진행하지만 integration까지 닫지 못한다.
- trace는 `partial + orchestration`으로 결과를 반환하고, packet/contracts에 대한 feedback을 남긴다.

### 3. 첫 operator decision + snapshot

- operator는 실패를 "구현자 잘못"으로 처리하지 않고 `rework` decision을 남긴다.
- 같은 시점의 control-plane 상태는 snapshot ledger로 고정한다.

### 4. 두 번째 handoff

- operator는 packet 입력을 보강한 새 packet을 다시 발행한다.
- 여기서 `support/editor-command-surface.md` 같은 보조 입력 문서를 handoff에 추가한다.

### 5. 두 번째 trace

- impl actor는 보강된 입력 기준으로 구현을 마무리하고 `success`를 반환한다.
- 다만 slice 전체 완료가 아니라, operator가 다음 integration handoff를 발행할 수 있는 수준까지 도달한 상태다.

### 6. accept decision + current ledger

- operator는 `accept` decision을 남기고 current ledger를 갱신한다.
- current ledger는 최신 상태만 들고 있고, decision 시점 상태는 snapshot ledger에서 복원할 수 있다.

## 중요한 해석 규칙

- `parent_wbs` 값은 실제 WBS가 아니라 예시용 식별자다.
- 이 디렉터리는 "형태"와 "흐름"을 보여주기 위한 것이지, 현재 저장소에 이미 해당 slice WBS가 존재한다는 뜻은 아니다.
- 실제 WBS를 만들기 시작하면 `parent_wbs`, `slice_id`, `owned_paths`를 실제 값으로 바꿔야 한다.
- 예시 run은 `run-local seq`로 정렬된다. 시간값은 보조 정보다.

## 검증 방법

예시 JSON은 validator로 바로 검증할 수 있다.

```bash
python3 scripts/repo/validate_wbs_artifact.py \
  --kind handoff-packet \
  --file context/wbs/examples/runs/RUN-EX-2026-03-06-A/packets/0001.packet.EX-MVP-TS-INSERT.impl.json
```

또는 테스트 전체를 실행한다.

```bash
python3 -m unittest scripts.repo.tests.test_validate_wbs_artifact \
  scripts.repo.tests.test_wbs_example_artifacts -v
```
