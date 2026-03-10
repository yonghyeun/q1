# DEC: Keep wrapper-first action routing in root `AGENTS.md` and future skills, not in a dedicated policy document

- Date: 2026-03-09
- Related to: `2026-03-09_wrapper-first-agent-actions-and-gate-remediation.md`
- Context: wrapper-first와 gate remediation 원칙 자체는 유지하기로 했지만, 이를 `policies/agent-action-policy.md` 같은 별도 policy 문서로 두는 방식은 중복 우려가 생겼다. issue, PR, merge, worktree 같은 액션의 실제 실행 경로는 앞으로 skill과 wrapper가 더 직접적으로 담당할 예정이고, skill frontmatter와 `SKILL.md`가 실행 지침을 설명하는 더 자연스러운 위치라고 판단했다.
- Decision: wrapper-first action routing과 gate remediation은 별도 policy 문서로 분리하지 않는다.
  - 저장소 공통 선언은 루트 `AGENTS.md`에 최소 규칙만 남긴다.
  - 실제 실행 지침, wrapper 사용 순서, 세부 행동 가이드는 향후 skill과 그 frontmatter에서 설명한다.
  - `policies/agent-action-policy.md`는 제거한다.
- Alternatives: wrapper-first와 gate remediation 원칙을 별도 policy 문서로 유지한다. 실행 지침을 모두 루트 `AGENTS.md`에 상세하게 적는다. skill 없이 문서와 주의력만으로 raw 명령 우회를 관리한다.
- Tradeoffs: policy 문서 하나를 줄여 구조는 단순해지지만, skill이 없는 맥락에서는 실행 지침의 상세도가 낮아질 수 있다. 반대로 별도 policy 문서를 유지하면 repo-level SoT는 늘어나지만, gate 문서와 wrapper, 향후 skill 설명 사이에 중복이 생길 가능성이 커진다.
- Revisit if: skill 기반 액션 라우팅을 실제로 쓰지 않게 되거나, wrapper 사용 규칙을 저장소 차원의 policy로 다시 승격하는 편이 운영상 더 명확하다고 판단될 때.
