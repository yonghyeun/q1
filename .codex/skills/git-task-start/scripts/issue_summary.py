#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from typing import Any


SECTION_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
CODE_RE = re.compile(r"`([^`]+)`")
CHECKLIST_RE = re.compile(r"^\s*[-*]\s+\[(?: |x|X)\]\s+(.*)$")
LABEL_RE = re.compile(r"^(status|priority|area|type):")


@dataclass
class IssueSummary:
    goal: str
    done: str
    constraints: str
    first_steps: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render a compact task-start issue summary.")
    parser.add_argument("--json-file", help="Path to a GitHub issue JSON payload. Reads stdin when omitted.")
    return parser.parse_args()


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json_file:
        with open(args.json_file, "r", encoding="utf-8") as handle:
            return json.load(handle)
    return json.load(sys.stdin)


def split_sections(body: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    matches = list(SECTION_RE.finditer(body))
    if not matches:
        return sections

    for index, match in enumerate(matches):
        title = match.group(1).strip().lower()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        sections[title] = body[start:end].strip()
    return sections


def clean_text(raw: str) -> str:
    text = raw.strip()
    if not text:
        return ""
    text = CODE_RE.sub(r"\1", text)
    lines: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        stripped = re.sub(r"^[-*]\s+", "", stripped)
        stripped = re.sub(r"^\d+\.\s+", "", stripped)
        stripped = re.sub(r"\s+", " ", stripped)
        lines.append(stripped)
    return " ".join(lines)


def first_sentence(raw: str) -> str:
    text = clean_text(raw)
    if not text:
        return ""
    parts = re.split(r"(?<=[.!?])\s+|(?<=다\.)\s+|(?<=요\.)\s+", text, maxsplit=1)
    return parts[0].strip()


def first_list_items(raw: str, limit: int = 3) -> list[str]:
    items: list[str] = []
    for line in raw.splitlines():
        match = CHECKLIST_RE.match(line) or re.match(r"^\s*[-*]\s+(.*)$", line)
        if not match:
            continue
        item = clean_text(match.group(1))
        if item:
            items.append(item)
        if len(items) >= limit:
            break
    return items


def strip_issue_prefix(title: str) -> str:
    return re.sub(r"^\[[^]]+\]\s*", "", title).strip()


def format_labels(payload: dict[str, Any]) -> str:
    names = []
    for label in payload.get("labels", []):
        name = str(label.get("name", "")).strip()
        if name and LABEL_RE.match(name):
            names.append(name)
    if not names:
        return ""
    return ", ".join(names[:4])


def extract_goal(payload: dict[str, Any], sections: dict[str, str]) -> str:
    for key in ("goal", "summary", "operational problem", "context"):
        sentence = first_sentence(sections.get(key, ""))
        if sentence:
            return sentence
    return strip_issue_prefix(str(payload.get("title", "")).strip()) or "issue 목적 확인 필요."


def extract_done(payload: dict[str, Any], sections: dict[str, str]) -> str:
    done_items = first_list_items(sections.get("done signal", ""))
    if done_items:
        return "; ".join(done_items)

    body_checklists = first_list_items(str(payload.get("body", "")))
    if body_checklists:
        return "; ".join(body_checklists)

    goal = extract_goal(payload, sections)
    return f"{goal} 기준으로 완료 조건 재확인 필요."


def extract_constraints(payload: dict[str, Any], sections: dict[str, str]) -> str:
    constraint_items = first_list_items(sections.get("constraints", ""))
    if constraint_items:
        return "; ".join(constraint_items)

    out_of_scope = first_list_items(sections.get("out of scope", ""))
    labels = format_labels(payload)
    parts = out_of_scope[:2]
    if labels:
        parts.append(f"라벨: {labels}")
    if parts:
        return "; ".join(parts)
    return "명시된 제약 부족. core wrapper 경계와 네트워크 승인 흐름 유지."


def extract_first_steps(payload: dict[str, Any], sections: dict[str, str]) -> str:
    affected_items = first_list_items(sections.get("affected surface", ""), limit=2)
    steps: list[str] = []
    if affected_items:
        joined = ", ".join(affected_items)
        steps.append(f"영향 범위 확인: {joined}")

    goal = clean_text(sections.get("goal", ""))
    if goal:
        steps.append(f"출력 흐름 설계: {first_sentence(goal)}")

    constraints = clean_text(sections.get("constraints", ""))
    if "fallback" in constraints.lower() or "fallback" in str(payload.get("body", "")).lower():
        steps.append("fallback 정의: issue body 부족 시 title/labels/checklist 기반 요약")

    if not steps:
        title = strip_issue_prefix(str(payload.get("title", "")).strip()) or "issue 확인"
        steps.append(f"이슈 재확인: {title}")

    return "; ".join(steps[:3])


def build_summary(payload: dict[str, Any]) -> IssueSummary:
    body = str(payload.get("body", "") or "")
    sections = split_sections(body)
    return IssueSummary(
        goal=extract_goal(payload, sections),
        done=extract_done(payload, sections),
        constraints=extract_constraints(payload, sections),
        first_steps=extract_first_steps(payload, sections),
    )


def render(payload: dict[str, Any]) -> str:
    summary = build_summary(payload)
    number = payload.get("number")
    title = str(payload.get("title", "")).strip()

    lines = ["Issue Summary"]
    if number or title:
        header = []
        if number:
            header.append(f"#{number}")
        if title:
            header.append(title)
        lines.append(f"- 이슈: {' '.join(header)}")
    lines.append(f"- 목적: {summary.goal}")
    lines.append(f"- 완료 조건: {summary.done}")
    lines.append(f"- 제약/주의: {summary.constraints}")
    lines.append(f"- 첫 작업 후보: {summary.first_steps}")
    return "\n".join(lines)


def main() -> int:
    payload = load_payload(parse_args())
    print(render(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
