# Editor Command Surface Note

이 문서는 `EX-MVP-TS-INSERT` 예시 handoff의 보조 입력이다.

예시 의도는 "operator가 packet을 보강할 때 어떤 보조 문맥을 추가할 수 있는가"를 보여주는 것이다.

## 최소 계약

- `playerTimeAdapter.getCurrentSeconds(): number`
- `noteEditor.insertAtCursor(markdown: string): void`
- 현재 handoff에서는 analytics emission을 구현 범위에 포함하지 않는다.

## 구현 경계

- impl actor는 `timestamp_seconds -> markdown` 변환과 `insertAtCursor` 호출까지만 책임진다.
- analytics emission과 최종 UI wiring은 다음 integration handoff에서 다룬다.
