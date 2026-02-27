# SoT: Codex Runtime Source

`agent-team/sot/`는 Codex 실행 파일(`.codex/`)의 단일 원천이다.

## 원칙
- 역할 프롬프트 원본은 `agent-team/sot/agents/*.md`에 둔다.
- 역할/정책 변경은 `agent-team/`와 `agent-team/sot/codex-runtime.manifest.toml`에서만 수행한다.
- `.codex/config.toml`, `.codex/agents/*.md`, `.codex/agents/*.toml`은 생성 결과물로 취급한다.
- 생성 결과를 수동 편집하지 않는다.

## 동기화 절차
1. SoT 파일 수정
2. `python3 agent-team/scripts/generate_codex_runtime.py` 실행
3. `python3 agent-team/scripts/verify_codex_runtime_sync.py` 통과 확인
4. SoT 변경과 생성 결과를 함께 커밋
