# DEC: gh read-only approval allow candidates

- Date: 2026-03-11
- Context: Codex 운영 중 `gh auth status`, `gh issue view`, `gh issue list`, `gh pr view` 같은 조회성 명령도 반복 승인이나 권한 상승이 필요해 issue/PR 확인 흐름이 자주 끊긴다. 반면 저장소 스크립트만으로 sandbox 정책 자체를 바꿀 수는 없다.
- Decision: approval allow 후보는 read-only prefix인 `gh auth status`, `gh issue view`, `gh issue list`, `gh pr view`로 한정한다. `gh issue edit`, `gh issue create`, `gh pr create`, `gh pr edit`, `gh pr merge`, 범용 `gh api` 같은 write 또는 범위 불명확 명령은 제외 범위로 유지한다.
- Alternatives: 현 상태를 유지해 매번 승인한다. 또는 `gh issue`, `gh pr`처럼 더 넓은 prefix를 allow 후보로 잡는다.
- Tradeoffs: 조회 흐름 마찰은 줄어든다. 대신 GitHub 메타데이터 read 범위는 넓어진다. 넓은 prefix를 피해서 write 승인 경계는 유지한다.
- Revisit if: approval 시스템이 read-only capability를 더 세밀하게 구분하거나, 실제 운영에서 추가 read-only 조회 명령이 반복적으로 필요한 것이 확인되면 후보 집합을 다시 검토한다.
