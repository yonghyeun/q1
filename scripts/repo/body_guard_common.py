from __future__ import annotations

import re
from pathlib import Path


EXIT_INVALID_BODY = 40

PLACEHOLDER_PATTERNS = [
    re.compile(r"Closes #<issue-number>", re.IGNORECASE),
    re.compile(r"<issue-number>", re.IGNORECASE),
    re.compile(r"^\s*-\s*Related:\s*#\s*$", re.IGNORECASE | re.MULTILINE),
    re.compile(r"<!--"),
]


class BodyQualityError(Exception):
    pass


def with_next_action(message: str, next_action: str) -> str:
    return f"{message}\n다음 행동: {next_action}"


def read_text(path: Path) -> str:
    if not path.exists():
        raise BodyQualityError(
            with_next_action(
                f"본문 파일을 찾을 수 없습니다: {path}",
                "body 파일 경로를 다시 확인하고, 템플릿을 채운 파일을 전달.",
            )
        )
    return path.read_text(encoding="utf-8")


def ensure_required_headings(body: str, headings: list[str]) -> None:
    missing = [heading for heading in headings if heading not in body]
    if missing:
        joined = ", ".join(missing)
        raise BodyQualityError(
            with_next_action(
                f"필수 섹션이 누락되었습니다: {joined}",
                "해당 템플릿의 누락 섹션을 추가하고 각 섹션을 템플릿 순서대로 다시 채움.",
            )
        )


def iter_sections(body: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current = "__preamble__"
    sections[current] = []

    for line in body.splitlines():
        if line.startswith("## "):
            current = line.strip()
            sections.setdefault(current, [])
            continue
        sections.setdefault(current, []).append(line)

    return {key: "\n".join(value).strip() for key, value in sections.items()}


def has_meaningful_text(text: str) -> bool:
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue

        if re.match(r"^[-*]\s*$", line):
            continue
        if re.match(r"^[-*]\s*\[[ xX]\]\s*$", line):
            continue
        if re.match(r"^\d+\.\s*$", line):
            continue

        cleaned = re.sub(r"^[-*]\s*", "", line)
        cleaned = re.sub(r"^\d+\.\s*", "", cleaned)
        cleaned = cleaned.strip()
        if len(cleaned) >= 2 and re.search(r"[0-9A-Za-z가-힣]", cleaned):
            return True
    return False


def ensure_no_placeholders(body: str) -> None:
    errors: list[str] = []
    for pattern in PLACEHOLDER_PATTERNS:
        if pattern.search(body):
            errors.append(pattern.pattern)

    for line in body.splitlines():
        striped = line.strip()
        if re.match(r"^[-*]\s*$", striped):
            errors.append("empty_bullet")
        if re.match(r"^[-*]\s*\[[ xX]\]\s*$", striped):
            errors.append("empty_checkbox")

    if errors:
        uniq = ", ".join(sorted(set(errors)))
        raise BodyQualityError(
            with_next_action(
                f"미완성 텍스트/플레이스홀더가 남아 있습니다: {uniq}",
                "placeholder를 실제 이슈 번호, 결정 내용, 검증 메모로 치환한 뒤 다시 실행.",
            )
        )


def validate_sections_have_content(body: str, headings: list[str]) -> None:
    sections = iter_sections(body)
    missing_content: list[str] = []
    for heading in headings:
        if not has_meaningful_text(sections.get(heading, "")):
            missing_content.append(heading)
    if missing_content:
        joined = ", ".join(missing_content)
        raise BodyQualityError(
            with_next_action(
                f"아래 섹션에 구체 내용이 필요합니다: {joined}",
                "빈 bullet만 두지 말고 정책상 요구되는 배경, 변경, 리스크, 판단 내용을 각 섹션에 채움.",
            )
        )
