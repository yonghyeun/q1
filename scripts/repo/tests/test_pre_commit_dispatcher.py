from __future__ import annotations

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[3]
DISPATCHER = ROOT_DIR / ".githooks/pre-commit"


class PreCommitDispatcherTests(unittest.TestCase):
    def make_repo(self) -> Path:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)

        root = Path(temp_dir.name)
        (root / ".githooks/pre-commit.d").mkdir(parents=True)
        shutil.copy2(DISPATCHER, root / ".githooks/pre-commit")

        subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True)
        return root

    def test_dispatcher_succeeds_when_no_hooklets_exist(self) -> None:
        root = self.make_repo()
        shutil.rmtree(root / ".githooks/pre-commit.d")

        result = subprocess.run(
            ["bash", str(root / ".githooks/pre-commit")],
            cwd=root,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)

    def test_dispatcher_runs_hooklets_in_name_order(self) -> None:
        root = self.make_repo()
        log_path = root / "hook-order.log"
        first = root / ".githooks/pre-commit.d/20-second"
        second = root / ".githooks/pre-commit.d/10-first"

        first.write_text(
            "#!/usr/bin/env bash\nset -euo pipefail\necho second >> hook-order.log\n",
            encoding="utf-8",
        )
        second.write_text(
            "#!/usr/bin/env bash\nset -euo pipefail\necho first >> hook-order.log\n",
            encoding="utf-8",
        )
        first.chmod(0o755)
        second.chmod(0o755)

        result = subprocess.run(
            ["bash", str(root / ".githooks/pre-commit")],
            cwd=root,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(log_path.read_text(encoding="utf-8").splitlines(), ["first", "second"])


if __name__ == "__main__":
    unittest.main()
