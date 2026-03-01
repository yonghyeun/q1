#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


EXIT_INVALID_BODY = 40

PR_REQUIRED_HEADINGS = [
    "## Issue Link (Required)",
    "## 목적 (Why)",
    "## 변경 요약 (What)",
    "## 범위",
    "## 영향도 / 리스크",
    "## 리뷰 포인트 (Reviewer Focus)",
    "## 참고 링크",
]

ISSUE_REQUIRED_HEADINGS = {
    "feature": [
        "## Task ID",
        "## Problem / Opportunity",
        "## Goal",
        "## In Scope",
        "## Out of Scope",
        "## Acceptance Criteria",
        "## Risks",
    ],
    "bug": [
        "## Task ID",
        "## Bug Summary",
        "## Reproduction Steps",
        "## Expected Behavior",
        "## Actual Behavior",
        "## Acceptance Criteria",
        "## Risks",
    ],
    "chore": [
        "## Task ID",
        "## Objective",
        "## Scope",
        "## Operational Impact",
        "## Acceptance Criteria",
        "## Risks",
    ],
}

PLACEHOLDER_PATTERNS = [
    re.compile(r"T-000N"),
    re.compile(r"Closes #<issue-number>", re.IGNORECASE),
    re.compile(r"<issue-number>", re.IGNORECASE),
    re.compile(r"<!--"),
]


class BodyQualityError(Exception):
    pass


def read_text(path: Path) -> str:
    if not path.exists():
        raise BodyQualityError(f"본문 파일을 찾을 수 없습니다: {path}")
    return path.read_text(encoding="utf-8")


def ensure_required_headings(body: str, headings: list[str]) -> None:
    missing = [heading for heading in headings if heading not in body]
    if missing:
        joined = ", ".join(missing)
        raise BodyQualityError(f"필수 섹션이 누락되었습니다: {joined}")


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

    return {k: "\n".join(v).strip() for k, v in sections.items()}


def has_meaningful_text(text: str) -> bool:
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue

        if re.match(r"^[-*]\s*$", line):
            continue
        if re.match(r"^[-*]\s*\[[ xX]\]\s*$", line):
            continue
        if re.match(r"^\d+\.\s*$", line):
            continue

        cleaned = re.sub(r"^[-*]\s*", "", line)
        cleaned = re.sub(r"^\d+\.\s*", "", cleaned)
        cleaned = cleaned.strip()
        if len(cleaned) >= 3 and re.search(r"[0-9A-Za-z가-힣]", cleaned):
            return True
    return False


def ensure_no_placeholders(body: str) -> None:
    errors: list[str] = []
    for pattern in PLACEHOLDER_PATTERNS:
        if pattern.search(body):
            errors.append(pattern.pattern)

    for line in body.splitlines():
        striped = line.strip()
        if re.match(r"^[-*]\s*$", striped):
            errors.append("empty_bullet")
        if re.match(r"^[-*]\s*\[[ xX]\]\s*$", striped):
            errors.append("empty_checkbox")

    if errors:
        uniq = ", ".join(sorted(set(errors)))
        raise BodyQualityError(f"미완성 텍스트/플레이스홀더가 남아 있습니다: {uniq}")


def ensure_issue_task_id(body: str) -> None:
    if not re.search(r"## Task ID\s*\n-\s*T-[0-9]{4}", body):
        raise BodyQualityError("Task ID 섹션에 유효한 T-0000 형식이 필요합니다.")


def ensure_close_keyword(body: str) -> None:
    if not re.search(r"\b(closes|fixes|resolves)\s*#\d+\b", body, flags=re.IGNORECASE):
        raise BodyQualityError("PR 본문에 Closes/Fixes/Resolves #N 링크가 필요합니다.")


def validate_sections_have_content(body: str, headings: list[str]) -> None:
    sections = iter_sections(body)
    missing_content: list[str] = []
    for heading in headings:
        if not has_meaningful_text(sections.get(heading, "")):
            missing_content.append(heading)
    if missing_content:
        joined = ", ".join(missing_content)
        raise BodyQualityError(f"아래 섹션에 구체 내용이 필요합니다: {joined}")


def validate_pr_body(body: str) -> None:
    ensure_required_headings(body, PR_REQUIRED_HEADINGS)
    ensure_no_placeholders(body)
    ensure_close_keyword(body)
    validate_sections_have_content(
        body,
        [
            "## 목적 (Why)",
            "## 변경 요약 (What)",
            "## 영향도 / 리스크",
            "## 리뷰 포인트 (Reviewer Focus)",
            "## 참고 링크",
        ],
    )
    ensure_required_headings(body, ["### In Scope", "### Out of Scope"])


def validate_issue_body(body: str, issue_type: str) -> None:
    required_headings = ISSUE_REQUIRED_HEADINGS[issue_type]
    ensure_required_headings(body, required_headings)
    ensure_no_placeholders(body)
    ensure_issue_task_id(body)
    validate_sections_have_content(
        body,
        [heading for heading in required_headings if heading != "## Acceptance Criteria"],
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Issue/PR 본문 품질 가드")
    parser.add_argument("--kind", choices=["issue", "pr"], required=True)
    parser.add_argument("--body-file", required=True)
    parser.add_argument("--issue-type", choices=["feature", "bug", "chore"])
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    body = read_text(Path(args.body_file))

    if args.kind == "issue":
        if not args.issue_type:
            raise BodyQualityError("--kind issue 에서는 --issue-type 이 필요합니다.")
        validate_issue_body(body, args.issue_type)
    else:
        validate_pr_body(body)

    print(f"✅ {args.kind} body quality valid: {args.body_file}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BodyQualityError as error:
        print(f"❌ {error}", file=sys.stderr)
        raise SystemExit(EXIT_INVALID_BODY)
