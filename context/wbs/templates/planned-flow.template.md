# Planned Flow Template

이 템플릿은 사람이 slice별 planned flow를 초안 작성하거나 검토할 때 사용한다.
현재는 packet/trace처럼 별도 schema를 두지 않았으므로, 먼저 이 템플릿으로 운영 규칙을 고정한다.
현재 기본 모드는 `compiled flow`가 아니라 `blueprint flow`다.

권장 저장 위치는 `context/wbs/flows/<slice_id>.flow.vN.md`다.

```yaml
flow_id: FLOW-SLICE-ID
flow_version: 1
planning_style: blueprint
parent_wbs: mvp-wbs/v1
slice_id: SLICE-ID
status: active
owner_role: operator
goal: 이 slice를 어떤 route로 완료시킬 것인가
why: 왜 이 route가 현재 slice에 맞는가
entry_node_id: impl
terminal_node_ids:
  - done
  - cancelled
nodes:
  - node_id: impl
    owner_role: impl
    purpose: 이 node의 목적
    planning_mode: local_after_packet
    packet_expectations:
      required_inputs:
        - contracts
        - acceptance_criteria
        - owned_scope
        - verification_requirements
      required_outputs:
        - code_changes
        - tests
        - trace_summary
    packet_blueprint:
      goal_hint: 이 node packet이 지향해야 할 목표
      concretization_rules:
        - owned_scope를 현재 node 목적에 맞는 owned_paths로 내린다
        - verification_requirements를 현재 node에서 요구할 required_tests로 내린다
      non_goals:
        - 이 node packet에서 하지 않을 것
      autonomy_boundary:
        - 세부 구현 순서는 actor가 packet 수신 후 계획한다
        - route 변경은 operator feedback으로 올린다
    allowed_decisions:
      - accept
      - rework
      - block
    exit_evidence:
      - 다음 actor가 판단 가능한 trace
  - node_id: integration
    owner_role: integration
    purpose: 이 node의 목적
    allowed_decisions:
      - accept
      - rework
      - block
  - node_id: done
    owner_role: operator
    purpose: slice 종료
transitions:
  - transition_id: impl_accept_to_integration
    from: impl
    decision: accept
    to: integration
    conditions:
      - impl AC evidence exists
  - transition_id: impl_rework_to_impl
    from: impl
    decision: rework
    to: impl
    conditions:
      - direction is correct
      - packet or input revision is sufficient
exception_loops:
  - loop_id: blocked_wait_contract
    enter_via:
      - impl -> block
    exit_rule: missing contract resolved
revisit_rules:
  - same node rework repeats twice without new input
runtime_usage:
  packet_linking:
    - packet inputs에 이 flow 문서 경로를 넣는다
    - packet goal/why에서 현재 node 목적을 드러낸다
  decision_linking:
    - operator는 선택한 transition을 review summary 또는 rationale에서 설명한다
  feedback_linking:
    - flow 수정 필요 피드백은 현재 schema 한계상 orchestration target으로 남긴다
notes:
  - 특이사항
```

## Notes

- 이 템플릿은 node별 상세 구현 계획을 미리 쓰는 용도가 아니다.
- WBS의 `owned_scope`, `verification_requirements`는 이 문서에서 node별 packet blueprint로 번역된다.
- 현재 문서는 route와 packet blueprint를 고정하고, actor 상세 계획은 packet 수신 후 local plan으로 남기는 방식을 기본값으로 둔다.
- 작성 책임 기본값은 `operator`다.
- packet이 이미 발행된 뒤 route가 바뀌면 새 버전을 만들어 이후 packet이 참조하게 한다.
- actor는 flow를 직접 수정하기보다 trace feedback으로 수정 필요성을 올리는 쪽을 기본값으로 둔다.
