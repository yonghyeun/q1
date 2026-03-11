# DEC: Issue type taxonomy를 feature bug chore로 고정

- Date: 2026-03-11
- Context: issue 템플릿과 분류 체계는 문제 성격 기준으로 단순해야 하고, 과도한 type 증가는 template, gate, triage 복잡도를 높인다.
- Decision: issue type은 `feature`, `bug`, `chore` 세 가지로 고정한다.
- Alternatives: `docs`, `ops`, `research`, `spike` 같은 추가 type 도입. type 없이 label만 사용.
- Tradeoffs: 세밀한 분류는 label에 맡겨야 한다. 대신 template, 검색, 생성 경로가 단순해진다.
- Revisit if: 특정 성격의 issue가 반복적으로 세 타입 어디에도 자연스럽게 들어가지 않아 별도 템플릿 필요성이 누적될 때.
