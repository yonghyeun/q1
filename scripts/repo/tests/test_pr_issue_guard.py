from __future__ import annotations

import unittest

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pr_issue_guard  # noqa: E402


class PrIssueGuardTests(unittest.TestCase):
    def test_parse_issue_numbers_from_pr_body(self) -> None:
        body = "Summary\n\nCloses #1234\nFixes #88"
        numbers = pr_issue_guard.parse_issue_numbers_from_pr_body(body)
        self.assertEqual(numbers, ["1234", "88"])

    def test_validate_pr_issue_link_success(self) -> None:
        numbers = pr_issue_guard.validate_pr_issue_link(
            pr_body="This PR updates policy\n\nCloses #1234",
        )
        self.assertEqual(numbers, ["1234"])

    def test_validate_pr_issue_link_missing_keyword(self) -> None:
        with self.assertRaises(pr_issue_guard.PrIssueGuardError) as ctx:
            pr_issue_guard.validate_pr_issue_link(
                pr_body="링크 키워드 없음",
            )
        self.assertEqual(ctx.exception.exit_code, pr_issue_guard.EXIT_LINK_MISSING)


if __name__ == "__main__":
    unittest.main()
