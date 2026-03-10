#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from body_guard_common import (  # type: ignore
    BodyQualityError,
    EXIT_INVALID_BODY,
    ensure_no_placeholders,
    ensure_required_headings,
    read_text,
    validate_sections_have_content,
)


PR_REQUIRED_HEADINGS = [
    "## Summary",
    "## Primary Issue",
    "## Related Issues",
    "## Context",
    "## Changes",
    "## Decisions Made",
    "## Deferred / Not Included",
    "## Validation Notes",
    "## Risks",
    "## Reviewer Focus",
]
def validate_pr_body(body: str) -> None:
    ensure_required_headings(body, PR_REQUIRED_HEADINGS)
    ensure_no_placeholders(body)
    validate_sections_have_content(
        body,
        [
            "## Summary",
            "## Primary Issue",
            "## Related Issues",
            "## Context",
            "## Changes",
            "## Decisions Made",
            "## Validation Notes",
            "## Risks",
            "## Reviewer Focus",
        ],
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="PR 본문 품질 가드")
    parser.add_argument("--body-file", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    body = read_text(Path(args.body_file))
    validate_pr_body(body)
    print(f"✅ pr body quality valid: {args.body_file}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BodyQualityError as error:
        print(f"❌ {error}", file=sys.stderr)
        raise SystemExit(EXIT_INVALID_BODY)
