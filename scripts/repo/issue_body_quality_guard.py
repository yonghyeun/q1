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


ISSUE_REQUIRED_HEADINGS = {
    "feature": [
        "## Summary",
        "## Context",
        "## Problem / Opportunity",
        "## Goal",
        "## Expected Impact",
        "## Constraints",
        "## Decision Candidates",
        "## Done Signal",
        "## Out of Scope",
        "## Related Links",
    ],
    "bug": [
        "## Summary",
        "## Context",
        "## Observed Behavior",
        "## Expected Behavior",
        "## Impact",
        "## Reproduction Clues",
        "## Suspected Area",
        "## Constraints",
        "## Decision Candidates",
        "## Done Signal",
        "## Related Links",
    ],
    "chore": [
        "## Summary",
        "## Context",
        "## Operational Problem",
        "## Goal",
        "## Affected Surface",
        "## Constraints",
        "## Decision Candidates",
        "## Done Signal",
        "## Out of Scope",
        "## Related Links",
    ],
}


def validate_issue_body(body: str, issue_type: str) -> None:
    required_headings = ISSUE_REQUIRED_HEADINGS[issue_type]
    ensure_required_headings(body, required_headings)
    ensure_no_placeholders(body)
    validate_sections_have_content(body, required_headings)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Issue 본문 품질 가드")
    parser.add_argument("--issue-type", choices=["feature", "bug", "chore"], required=True)
    parser.add_argument("--body-file", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    body = read_text(Path(args.body_file))
    validate_issue_body(body, args.issue_type)
    print(f"✅ issue body quality valid: {args.body_file}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BodyQualityError as error:
        print(f"❌ {error}", file=sys.stderr)
        raise SystemExit(EXIT_INVALID_BODY)
