#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from body_guard_common import iter_sections  # type: ignore

EXIT_LINK_MISSING = 4
EXIT_LINK_MISMATCH = 5


class PrIssueGuardError(Exception):
    def __init__(self, message: str, exit_code: int) -> None:
        super().__init__(message)
        self.exit_code = exit_code


def parse_issue_numbers_from_primary_issue_section(body: str) -> list[str]:
    primary_issue = iter_sections(body).get("## Primary Issue", "")
    pattern = re.compile(
        r"\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s+#(\d+)\b",
        re.IGNORECASE,
    )
    return pattern.findall(primary_issue)


def validate_pr_issue_link(pr_body: str, expected_issue_number: str | None = None) -> list[str]:
    linked_issue_numbers = parse_issue_numbers_from_primary_issue_section(pr_body)
    if not linked_issue_numbers:
        raise PrIssueGuardError(
            "Primary Issue 섹션에 이슈 자동 종료 키워드가 없습니다. 예: `Closes #1234`\n"
            "다음 행동: Primary Issue 섹션에 닫아야 할 대표 이슈를 close keyword와 함께 추가하고 다시 실행.",
            EXIT_LINK_MISSING,
        )

    if expected_issue_number is not None:
        mismatched_numbers = [number for number in linked_issue_numbers if number != expected_issue_number]
        if mismatched_numbers or expected_issue_number not in linked_issue_numbers:
            rendered_numbers = ", ".join(f"#{number}" for number in linked_issue_numbers)
            raise PrIssueGuardError(
                "Primary Issue 섹션의 대표 이슈와 local linked issue metadata가 일치하지 않습니다.\n"
                f"- PR body: {rendered_numbers}\n"
                f"- linked issue metadata: #{expected_issue_number}\n"
                "다음 행동: Primary Issue 섹션의 close keyword를 local linked issue metadata와 같은 이슈 번호로 맞춘 뒤 다시 실행.",
                EXIT_LINK_MISMATCH,
            )

    return linked_issue_numbers


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate PR close-link in body")
    body_group = parser.add_mutually_exclusive_group(required=True)
    body_group.add_argument("--pr-body", help="pull request body text")
    body_group.add_argument("--pr-body-file", help="path to pull request body file")
    parser.add_argument("--expected-issue-number", help="linked issue number recorded in local worktree metadata")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.pr_body_file:
        pr_body = Path(args.pr_body_file).read_text(encoding="utf-8")
    else:
        pr_body = args.pr_body or ""

    try:
        numbers = validate_pr_issue_link(
            pr_body=pr_body,
            expected_issue_number=args.expected_issue_number,
        )
        print(f"✅ PR issue link valid: {', '.join('#' + n for n in numbers)}")
        return 0
    except PrIssueGuardError as exc:
        print(f"❌ {exc}", file=sys.stderr)
        return exc.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
