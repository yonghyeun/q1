#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="git-task-end post-apply PR summary")
    parser.add_argument("--pr", required=True, help="Merged PR number or URL")
    parser.add_argument("--linked-issue-number")
    parser.add_argument("--linked-issue-title")
    return parser.parse_args()


def run_gh_pr_view(pr_target: str) -> dict[str, Any]:
    command = [
        "gh",
        "pr",
        "view",
        pr_target,
        "--json",
        "number,title,body,url,state,mergedAt,baseRefName,headRefName",
    ]
    result = subprocess.run(
        command,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        stderr = result.stderr.strip()
        print("❌ merged PR 요약 조회에 실패했습니다.", file=sys.stderr)
        if stderr:
            print(f"gh: {stderr}", file=sys.stderr)
        print(
            "다음 행동: gh 인증/네트워크 상태를 확인하고 같은 요약 helper를 다시 실행하세요.",
            file=sys.stderr,
        )
        raise SystemExit(1)

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as error:
        print(f"❌ PR 조회 결과를 해석할 수 없습니다: {error}", file=sys.stderr)
        raise SystemExit(1)


def iter_sections(body: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current = "__preamble__"
    sections[current] = []

    for line in body.splitlines():
        if line.startswith("## "):
            current = line.strip()
            sections.setdefault(current, [])
            continue
        sections.setdefault(current, []).append(line)

    return {key: "\n".join(value).strip() for key, value in sections.items()}


def split_meaningful_lines(text: str) -> list[str]:
    lines: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("<!--"):
            continue

        line = re.sub(r"^[-*]\s*", "", line)
        line = re.sub(r"^\d+\.\s*", "", line)
        line = re.sub(r"`", "", line)
        line = re.sub(r"\s+", " ", line).strip()
        if len(line) < 2:
            continue
        if not re.search(r"[0-9A-Za-z가-힣]", line):
            continue
        lines.append(line)
    return lines


def unique_limited(items: list[str], limit: int) -> list[str]:
    seen: set[str] = set()
    deduped: list[str] = []
    for item in items:
        normalized = item.strip()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        deduped.append(normalized)
        if len(deduped) >= limit:
            break
    return deduped


def strip_title_scope(title: str) -> str:
    return re.sub(r"^\[[^]]+\]\s*", "", title).strip()


def extract_issue_numbers(text: str) -> list[str]:
    return unique_limited(re.findall(r"#(\d+)", text), limit=3)


def select_change_purpose(
    title: str,
    summary_lines: list[str],
    linked_issue_number: str,
    linked_issue_title: str,
) -> str:
    if summary_lines:
        return summary_lines[0]
    if linked_issue_title:
        if linked_issue_number:
            return f"{linked_issue_title} 해결 흐름 정리 (issue #{linked_issue_number})"
        return f"{linked_issue_title} 해결 흐름 정리"
    stripped_title = strip_title_scope(title)
    if linked_issue_number:
        return f"{stripped_title} 반영 및 종료 요약 (issue #{linked_issue_number})"
    return stripped_title


def select_key_changes(title: str, sections: dict[str, str], summary_lines: list[str]) -> list[str]:
    changes = split_meaningful_lines(sections.get("## Changes", ""))
    if changes:
        return unique_limited(changes, limit=3)

    combined = summary_lines[1:] if len(summary_lines) > 1 else []
    if combined:
        return unique_limited(combined, limit=3)

    context_lines = split_meaningful_lines(sections.get("## Context", ""))
    if context_lines:
        return unique_limited(context_lines, limit=3)

    return [f"PR 제목 기준 fallback: {strip_title_scope(title)}"]


def select_impact_scope(pr: dict[str, Any], sections: dict[str, str]) -> list[str]:
    risks = split_meaningful_lines(sections.get("## Risks", ""))
    impact_lines = [line for line in risks if line.lower().startswith("impact:")]
    if impact_lines:
        return unique_limited(impact_lines, limit=2)

    validation_lines = split_meaningful_lines(sections.get("## Validation Notes", ""))
    if validation_lines:
        return unique_limited(validation_lines, limit=2)

    head = pr.get("headRefName") or "<unknown-head>"
    base = pr.get("baseRefName") or "<unknown-base>"
    return [f"{head} 변경이 {base} 에 반영됨", "task end apply 이후 cleanup까지 연동되는 종료 흐름"]


def select_follow_up_points(
    pr: dict[str, Any],
    sections: dict[str, str],
    linked_issue_number: str,
) -> list[str]:
    reviewer_focus = split_meaningful_lines(sections.get("## Reviewer Focus", ""))
    if reviewer_focus:
        return unique_limited(reviewer_focus, limit=3)

    deferred = split_meaningful_lines(sections.get("## Deferred / Not Included", ""))
    if deferred:
        return unique_limited(deferred, limit=3)

    points: list[str] = []
    if linked_issue_number:
        points.append(f"linked issue #{linked_issue_number} 종료 상태와 후속 커뮤니케이션 확인")
    if pr.get("state") == "MERGED" or pr.get("mergedAt"):
        points.append("merge 직후 공유용 요약과 release note 반영 여부 확인")
    points.append("PR 본문이 빈약하면 수동 배경 설명을 보강")
    return unique_limited(points, limit=3)


def render_summary(
    pr: dict[str, Any],
    linked_issue_number: str,
    linked_issue_title: str,
) -> str:
    body = pr.get("body") or ""
    sections = iter_sections(body)
    title = pr.get("title") or "<unknown-title>"
    summary_lines = split_meaningful_lines(sections.get("## Summary", ""))

    issue_numbers = extract_issue_numbers(sections.get("## Primary Issue", ""))
    resolved_issue = linked_issue_number or (issue_numbers[0] if issue_numbers else "")
    resolved_issue_title = linked_issue_title

    purpose = select_change_purpose(title, summary_lines, resolved_issue, resolved_issue_title)
    changes = select_key_changes(title, sections, summary_lines)
    impacts = select_impact_scope(pr, sections)
    follow_ups = select_follow_up_points(pr, sections, resolved_issue)

    lines = [
        "[git-task-end] Merged PR summary",
        f"- PR: #{pr.get('number')} {title}",
        f"- URL: {pr.get('url') or '<unknown-url>'}",
        f"- State: {pr.get('state') or '<unknown-state>'}",
    ]

    merged_at = pr.get("mergedAt")
    if merged_at:
        lines.append(f"- Merged at: {merged_at}")
    if resolved_issue:
        if resolved_issue_title:
            lines.append(f"- Linked issue: #{resolved_issue} {resolved_issue_title}")
        else:
            lines.append(f"- Linked issue: #{resolved_issue}")

    lines.extend(
        [
            "",
            f"변경 목적: {purpose}",
            "핵심 변경점:",
        ]
    )
    lines.extend(f"- {item}" for item in changes)
    lines.append("영향 범위:")
    lines.extend(f"- {item}" for item in impacts)
    lines.append("후속 확인 포인트:")
    lines.extend(f"- {item}" for item in follow_ups)
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    pr = run_gh_pr_view(args.pr)
    print(render_summary(pr, args.linked_issue_number or "", args.linked_issue_title or ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
