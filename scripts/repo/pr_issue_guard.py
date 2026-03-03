#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

EXIT_LINK_MISSING = 4


class PrIssueGuardError(Exception):
    def __init__(self, message: str, exit_code: int) -> None:
        super().__init__(message)
        self.exit_code = exit_code


def parse_issue_numbers_from_pr_body(body: str) -> list[str]:
    pattern = re.compile(
        r"\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s+#(\d+)\b",
        re.IGNORECASE,
    )
    return pattern.findall(body)


def validate_pr_issue_link(pr_body: str) -> list[str]:
    linked_issue_numbers = parse_issue_numbers_from_pr_body(pr_body)
    if not linked_issue_numbers:
        raise PrIssueGuardError(
            "PR 본문에 이슈 자동 종료 키워드가 없습니다. 예: `Closes #1234`",
            EXIT_LINK_MISSING,
        )

    return linked_issue_numbers


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate PR close-link in body")
    body_group = parser.add_mutually_exclusive_group(required=True)
    body_group.add_argument("--pr-body", help="pull request body text")
    body_group.add_argument("--pr-body-file", help="path to pull request body file")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.pr_body_file:
        pr_body = Path(args.pr_body_file).read_text(encoding="utf-8")
    else:
        pr_body = args.pr_body or ""

    try:
        numbers = validate_pr_issue_link(pr_body=pr_body)
        print(f"✅ PR issue link valid: {', '.join('#' + n for n in numbers)}")
        return 0
    except PrIssueGuardError as exc:
        print(f"❌ {exc}", file=sys.stderr)
        return exc.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
