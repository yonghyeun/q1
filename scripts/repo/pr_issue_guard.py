#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from branch_guard import BranchPolicyError, load_rules, validate_branch_name

EXIT_LINK_MISSING = 4
EXIT_LINK_MISMATCH = 5


class PrIssueGuardError(Exception):
    def __init__(self, message: str, exit_code: int) -> None:
        super().__init__(message)
        self.exit_code = exit_code


def parse_issue_numbers_from_pr_body(body: str) -> list[str]:
    # GitHub auto-close keywords
    pattern = re.compile(
        r"\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s+#(\d+)\b",
        re.IGNORECASE,
    )
    return pattern.findall(body)


def validate_pr_issue_link(branch: str, pr_body: str, rules_path: Path) -> str:
    try:
        rules = load_rules(rules_path)
        meta = validate_branch_name(branch, rules)
    except BranchPolicyError as exc:
        raise PrIssueGuardError(str(exc), exc.exit_code) from exc

    linked_issue_numbers = parse_issue_numbers_from_pr_body(pr_body)
    if not linked_issue_numbers:
        raise PrIssueGuardError(
            "PR 본문에 이슈 자동 종료 키워드가 없습니다. 예: `Closes #1234`",
            EXIT_LINK_MISSING,
        )

    if meta.issue_number not in linked_issue_numbers:
        raise PrIssueGuardError(
            "PR 본문의 이슈 번호가 브랜치 issue와 일치하지 않습니다. "
            f"branch=i{meta.issue_number}, body={linked_issue_numbers}",
            EXIT_LINK_MISMATCH,
        )

    return meta.issue_number


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate PR issue link against branch")
    parser.add_argument("--branch", required=True, help="branch name")
    parser.add_argument(
        "--rules",
        default="policies/branch-policy.rules.json",
        help="branch policy rules path",
    )
    body_group = parser.add_mutually_exclusive_group(required=True)
    body_group.add_argument("--pr-body", help="pull request body text")
    body_group.add_argument("--pr-body-file", help="path to pull request body file")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    rules_path = Path(args.rules)
    if args.pr_body_file:
        pr_body = Path(args.pr_body_file).read_text(encoding="utf-8")
    else:
        pr_body = args.pr_body or ""

    try:
        issue_number = validate_pr_issue_link(
            branch=args.branch,
            pr_body=pr_body,
            rules_path=rules_path,
        )
        print(f"✅ PR issue link valid: branch issue #{issue_number}")
        return 0
    except PrIssueGuardError as exc:
        print(f"❌ {exc}", file=sys.stderr)
        return exc.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
