from __future__ import annotations

import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import issue_label_guard as guard  # noqa: E402


class IssueLabelGuardTests(unittest.TestCase):
    def test_build_issue_labels_success(self) -> None:
        labels = guard.build_issue_labels(
            issue_type="feature",
            status="inbox",
            priority="p2",
            areas=["repo", "docs"],
            source_type="agent-team",
        )
        self.assertEqual(
            labels,
            [
                "type:feature",
                "status:inbox",
                "priority:p2",
                "source_type:agent-team",
                "area:repo",
                "area:docs",
            ],
        )

    def test_build_issue_labels_deduplicates_area(self) -> None:
        labels = guard.build_issue_labels(
            issue_type="bug",
            status="ready",
            priority="p1",
            areas=["repo", "repo"],
            source_type="runtime-observation",
        )
        self.assertEqual(labels.count("area:repo"), 1)

    def test_build_issue_labels_rejects_unknown_area(self) -> None:
        with self.assertRaises(guard.BodyQualityError):
            guard.build_issue_labels(
                issue_type="chore",
                status="active",
                priority="p0",
                areas=["wbs"],
                source_type="human-request",
            )

    def test_build_issue_labels_requires_source_type(self) -> None:
        with self.assertRaises(guard.BodyQualityError):
            guard.build_issue_labels(
                issue_type="feature",
                status="blocked",
                priority="p3",
                areas=["agent-team"],
                source_type="backlog-migration",
            )


if __name__ == "__main__":
    unittest.main()
