# Structured Output Enforcement

이 문서는 WBS 오케스트레이션 산출물에서
`template` 기반 접근과 `Codex structured output` 강제 접근을 어떻게 함께 쓸지 정의한다.

## 조사 결론

현재 로컬 Codex 환경에서는 두 종류의 제어가 가능하다.

1. `~/.codex/config.toml`의 profile / developer instructions
2. `codex exec --output-schema <schema.json>`

이 둘은 강도가 다르다.

- profile / developer instructions는 **출력 형식을 유도하는 soft constraint**다.
- `--output-schema`는 non-interactive 실행에서 **최종 응답 shape를 강제하는 hard constraint**다.

즉, "config만으로 structured output을 강제"하는 것은 현재 구조상 적합하지 않다.

## 표준적 선택지

### A. 템플릿만 사용

- 장점: 사람이 읽고 수정하기 쉽다
- 단점: 형식 drift를 막기 어렵다

### B. Codex config/profile만 사용

- 장점: 별도 스키마 파일 없이 빠르게 시작할 수 있다
- 단점: interactive 응답은 여전히 서술형으로 흐를 수 있어 hard guarantee가 없다

### C. `codex exec --output-schema`만 사용

- 장점: 자동화에 가장 유리하다
- 단점: 사람이 직접 읽고 수정하는 문서로는 불편할 수 있다

### D. 템플릿 + JSON Schema + validator 하이브리드

- 장점: 사람 친화성과 기계 강제를 함께 얻는다
- 단점: template, schema, validator 세 레이어를 함께 유지해야 한다

현재 저장소에는 **D안**을 기본 추천으로 둔다.

## 권장 운영 모델

### 1. 사람 작성 경로

- 사람이 직접 packet / trace / ledger를 만들거나 검토할 때는 `templates/`를 사용한다.
- 템플릿은 human-readable 문서의 기준 포맷이다.

### 2. 에이전트 생성 경로

- 에이전트가 산출물을 생성할 때는 `codex exec --output-schema`를 사용한다.
- 생성 결과는 JSON schema를 통과하는 machine-readable artifact여야 한다.

### 3. 검증 경로

- 생성된 JSON artifact는 validator script로 다시 검증한다.
- 이 검증은 schema 위반뿐 아니라 일부 semantic rule도 체크한다.

## 왜 config-only를 권장하지 않나

- profile의 `Default response format`은 model에게 형식을 **권장**할 뿐이다.
- handoff packet, trace, run ledger는 orchestration control-plane의 입력값이므로, 형식 drift를 허용하면 안 된다.
- 따라서 사람이 읽기 좋은 응답 형식과, 기계가 신뢰할 수 있는 artifact 형식을 분리하는 편이 낫다.

## 권장 파일 구조

- `context/wbs/templates/`: 사람이 읽고 채우는 템플릿
- `context/wbs/schemas/`: `codex exec --output-schema`에 넘길 JSON Schema
- `scripts/repo/codex_wbs_emit.sh`: schema 강제 생성 래퍼
- `scripts/repo/validate_wbs_artifact.py`: schema + semantic validator

## 추천 워크플로우

### 수동 작성 / 토론

1. 템플릿을 복사해 초안을 만든다
2. 사람이 토론하며 필드를 보완한다
3. 필요 시 JSON artifact로 승격한다

### 자동 생성 / 반복 작업

1. prompt 파일을 만든다
2. `codex_wbs_emit.sh`로 schema 강제 생성한다
3. validator로 결과를 확인한다
4. 검토 후 run ledger에 반영한다

## 이 저장소 기준 결론

- handoff/trace/ledger는 **template만으로 운영하지 않는다**
- global Codex config도 **hard enforcement 수단으로 보지 않는다**
- 반복 생성이 필요한 곳은 `schema + validator + harness`를 우선 적용한다
- 사람 검토와 토론이 필요한 곳은 `template`을 같이 둔다
