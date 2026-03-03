from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pr_issue_guard  # noqa: E402


RULES_JSON = """{
  "policy_version": "v2.0.0",
  "default_branch": "main",
  "branch_regex": "^task/i[0-9]+-T-[0-9]{4}-[a-z0-9]+(?:-[a-z0-9]+)*$",
  "issue_token_regex": "^i[0-9]+$",
  "task_id_regex": "^T-[0-9]{4}$",
  "reserved_branches": ["main"],
  "required_context_for_push": ["context/tasks/{task_id}"],
  "required_artifacts_for_pr": ["context.md", "result.md"]
}"""


class PrIssueGuardTests(unittest.TestCase):
    def test_parse_issue_numbers_from_pr_body(self) -> None:
        body = "Summary\n\nCloses #1234\nFixes #88"
        numbers = pr_issue_guard.parse_issue_numbers_from_pr_body(body)
        self.assertEqual(numbers, ["1234", "88"])

    def test_validate_pr_issue_link_success(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            rules_path = Path(temp_dir) / "rules.json"
            rules_path.write_text(RULES_JSON, encoding="utf-8")
            issue = pr_issue_guard.validate_pr_issue_link(
                branch="task/i1234-T-0001-branch-governance",
                pr_body="This PR updates policy\n\nCloses #1234",
                rules_path=rules_path,
            )
            self.assertEqual(issue, "1234")

    def test_validate_pr_issue_link_missing_keyword(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            rules_path = Path(temp_dir) / "rules.json"
            rules_path.write_text(RULES_JSON, encoding="utf-8")
            with self.assertRaises(pr_issue_guard.PrIssueGuardError) as ctx:
                pr_issue_guard.validate_pr_issue_link(
                    branch="task/i1234-T-0001-branch-governance",
                    pr_body="링크 키워드 없음",
                    rules_path=rules_path,
                )
            self.assertEqual(ctx.exception.exit_code, pr_issue_guard.EXIT_LINK_MISSING)

    def test_validate_pr_issue_link_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            rules_path = Path(temp_dir) / "rules.json"
            rules_path.write_text(RULES_JSON, encoding="utf-8")
            with self.assertRaises(pr_issue_guard.PrIssueGuardError) as ctx:
                pr_issue_guard.validate_pr_issue_link(
                    branch="task/i1234-T-0001-branch-governance",
                    pr_body="Closes #9999",
                    rules_path=rules_path,
                )
            self.assertEqual(ctx.exception.exit_code, pr_issue_guard.EXIT_LINK_MISMATCH)


if __name__ == "__main__":
    unittest.main()
