from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import detached_head_guard  # noqa: E402


class DetachedHeadGuardTests(unittest.TestCase):
    def test_validate_write_allows_named_head(self) -> None:
        detached_head_guard.validate_not_detached("feature/add-guard")

    def test_validate_write_rejects_detached_head(self) -> None:
        with self.assertRaises(detached_head_guard.DetachedHeadError) as ctx:
            detached_head_guard.validate_not_detached("HEAD")
        self.assertEqual(
            ctx.exception.exit_code,
            detached_head_guard.EXIT_DETACHED_HEAD,
        )


if __name__ == "__main__":
    unittest.main()
