#!/usr/bin/env python3
from __future__ import annotations

import argparse
import difflib
from pathlib import Path
import subprocess
import tempfile
import tomllib


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify generated .codex runtime is in sync")
    parser.add_argument(
        "--manifest",
        default="agent-team/sot/codex-runtime.manifest.toml",
        help="Manifest path",
    )
    parser.add_argument(
        "--runtime-dir",
        default=".codex",
        help="Existing runtime directory to verify",
    )
    return parser.parse_args()


def read_manifest(manifest_path: Path) -> dict:
    with manifest_path.open("rb") as file:
        return tomllib.load(file)


def expected_files(manifest: dict) -> list[str]:
    files = ["config.toml"]
    for profile in manifest["profiles"].values():
        files.append(f'agents/{profile["prompt_output"]}')
    for agent in manifest["agents"].values():
        files.append(f'agents/{agent["toml_output"]}')
    files.append(f'agents/{manifest["task_template"]["prompt_output"]}')
    return sorted(set(files))


def compare_file(expected_path: Path, actual_path: Path, rel_path: str) -> list[str]:
    issues: list[str] = []
    if not actual_path.exists():
        issues.append(f"[MISSING] {rel_path}")
        return issues

    expected = expected_path.read_text(encoding="utf-8")
    actual = actual_path.read_text(encoding="utf-8")
    if expected == actual:
        return issues

    issues.append(f"[DIFF] {rel_path}")
    diff = difflib.unified_diff(
        actual.splitlines(),
        expected.splitlines(),
        fromfile=f"actual/{rel_path}",
        tofile=f"expected/{rel_path}",
        lineterm="",
    )
    issues.extend(list(diff))
    return issues


def main() -> int:
    args = parse_args()
    repo_root = Path.cwd().resolve()
    manifest_path = (repo_root / args.manifest).resolve()
    runtime_dir = (repo_root / args.runtime_dir).resolve()
    generate_script = (repo_root / "agent-team/scripts/generate_codex_runtime.py").resolve()

    manifest = read_manifest(manifest_path)
    targets = expected_files(manifest)

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        subprocess.run(
            [
                "python3",
                str(generate_script),
                "--manifest",
                str(manifest_path),
                "--output-dir",
                str(temp_path),
            ],
            check=True,
            cwd=repo_root,
        )

        issues: list[str] = []
        for rel_path in targets:
            expected_path = temp_path / rel_path
            actual_path = runtime_dir / rel_path
            issues.extend(compare_file(expected_path, actual_path, rel_path))

    if issues:
        print("❌ .codex 런타임 파일이 SoT와 동기화되지 않았습니다.")
        print("실행: python3 agent-team/scripts/generate_codex_runtime.py")
        for issue in issues:
            print(issue)
        return 1

    print("✅ .codex 런타임 파일이 SoT와 동기화되었습니다.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
