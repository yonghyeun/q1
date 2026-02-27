# Example: First ADLC Cycle

## 1) Explore
- Input: `task-brief.template.json`
- Owner: `planner-pm`
- Output: refined problem statement + interview hypothesis
- Gate: human approval required

## 2) Design
- Input: approved explore output
- Owner: `adlc-leader`
- Output: `leader-plan.template.json` style plan
- Gate: human approval required

## 3) Execute
- Input: approved leader plan + `handoff-packet.template.json`
- Owner: `builder`
- Output: draft artifact
- Review: `reviewer` validates against acceptance checks
- Gate: human approval required

## 4) Improve
- Input: `run-report.template.json` + optional `feedback-record.template.json`
- Owner: `adlc-leader` + `context-maintainer`
- Output: retry plan or weekly batch candidate
- Gate: human approval required
