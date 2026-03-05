# Experiments

배포 기반 실험 로그를 저장한다.

목표: "무엇을 왜 바꿨고, 결과가 어땠고, 다음에 무엇을 할지"를 5분 안에 복기 가능하게 만든다.

## 파일 네이밍(권장)

- `YYYY-MM-DD_slug.md`
- 예: `2026-03-03_timestamp-hotkey-hint.md`

## 템플릿

```md
# EXP: <title>

- Date: YYYY-MM-DD
- Hypothesis: H?
- Change: (변경 1개)
- Audience: (신규/전체/조건)
- Window: (예: 7일)
- Success metric: (Primary 1개)
- Guardrails: (최대 2개)

## Result

- (수치/관찰)

## Interpretation

- (왜 이렇게 나왔는지, 가능한 설명 2~3개)

## Decision

- Ship / Iterate / Revert / Pivot

## Next

- 다음 실험 1개
```

