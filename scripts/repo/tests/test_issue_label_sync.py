from __future__ import annotations

import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import issue_label_sync as sync  # noqa: E402


class IssueLabelSyncTests(unittest.TestCase):
    def test_build_commands_contains_all_labels(self) -> None:
        commands = sync.build_commands()
        self.assertEqual(len(commands), 20)
        self.assertEqual(commands[0][:4], ["gh", "label", "create", "type:feature"])
        self.assertEqual(commands[-1][:4], ["gh", "label", "create", "source_type:wbs-planned"])


if __name__ == "__main__":
    unittest.main()
