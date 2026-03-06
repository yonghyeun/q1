from __future__ import annotations

from pathlib import Path
import unittest
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import validate_wbs_artifact  # noqa: E402


class WbsExampleArtifactTests(unittest.TestCase):
    @staticmethod
    def infer_kind(path: Path) -> str:
        name = path.name
        if ".packet." in name:
            return "handoff-packet"
        if ".trace." in name:
            return "trace-summary"
        if ".decision." in name:
            return "operator-decision"
        if name.endswith("run-ledger.json"):
            return "run-ledger"
        raise AssertionError(f"지원하지 않는 example artifact kind: {path}")

    def test_all_example_json_artifacts_are_valid(self) -> None:
        repo_root = Path(__file__).resolve().parents[3]
        example_paths = sorted((repo_root / "context" / "wbs" / "examples").rglob("*.json"))
        self.assertTrue(example_paths, "검증할 example JSON artifact 가 없습니다.")

        for path in example_paths:
            kind = self.infer_kind(path)
            self.assertIn(kind, validate_wbs_artifact.KIND_TO_SCHEMA, f"지원하지 않는 artifact kind: {path}")
            with self.subTest(path=str(path.relative_to(repo_root))):
                payload = validate_wbs_artifact.load_json(path)
                validate_wbs_artifact.validate_against_schema(kind, payload)
                validate_wbs_artifact.validate_semantics(kind, payload)


if __name__ == "__main__":
    unittest.main()
