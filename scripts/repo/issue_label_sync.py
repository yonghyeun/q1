#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from issue_label_taxonomy import LABEL_SPECS


ROOT_DIR = Path(__file__).resolve().parents[2]


def build_commands() -> list[list[str]]:
    commands: list[list[str]] = []
    for spec in LABEL_SPECS:
        commands.append(
            [
                "gh",
                "label",
                "create",
                spec.name,
                "--color",
                spec.color,
                "--description",
                spec.description,
                "--force",
            ]
        )
    return commands


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="GitHub issue label sync")
    parser.add_argument("--apply", action="store_true", help="실제 원격 label 생성/갱신")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    commands = build_commands()

    if not args.apply:
        print("[issue-label-sync] Dry run")
        for command in commands:
            print("- " + " ".join(command))
        return 0

    subprocess.run(["bash", str(ROOT_DIR / "scripts" / "repo" / "gh_preflight.sh")], check=True)
    for command in commands:
        subprocess.run(command, check=True)

    print(f"✅ issue label sync 완료: {len(commands)}개")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
