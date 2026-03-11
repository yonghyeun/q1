#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass


TYPE_VALUES = ("feature", "bug", "chore")
STATUS_VALUES = ("inbox", "ready", "active", "blocked", "cancelled")
PRIORITY_VALUES = ("p0", "p1", "p2", "p3")
AREA_VALUES = ("product", "repo", "docs", "agent-team")
SOURCE_TYPE_VALUES = (
    "human-request",
    "agent-team",
    "runtime-observation",
    "wbs-planned",
)


@dataclass(frozen=True)
class LabelSpec:
    name: str
    color: str
    description: str


LABEL_SPECS = (
    LabelSpec("type:feature", "1d76db", "기능 요청과 기능 개선 backlog"),
    LabelSpec("type:bug", "d73a4a", "기대 동작과 실제 동작이 다른 backlog"),
    LabelSpec("type:chore", "6f42c1", "운영, 정책, 자동화, 저장소 정비 backlog"),
    LabelSpec("status:inbox", "ededed", "아직 정리 전인 backlog 입력"),
    LabelSpec("status:ready", "0e8a16", "실행 가능한 상태로 정리 완료"),
    LabelSpec("status:active", "fbca04", "현재 작업 중인 상태"),
    LabelSpec("status:blocked", "b60205", "외부 입력이나 의존성 부족으로 진행 불가"),
    LabelSpec("status:cancelled", "ffffff", "진행하지 않기로 결정된 backlog"),
    LabelSpec("priority:p0", "b60205", "가장 높은 우선순위"),
    LabelSpec("priority:p1", "d93f0b", "높은 우선순위"),
    LabelSpec("priority:p2", "fbca04", "기본 우선순위"),
    LabelSpec("priority:p3", "c2e0c6", "낮은 우선순위"),
    LabelSpec("area:product", "0052cc", "제품 기능과 사용자 동작 영역"),
    LabelSpec("area:repo", "5319e7", "저장소 구조, 스크립트, GitHub 운영 영역"),
    LabelSpec("area:docs", "0366d6", "문서와 정보 구조 영역"),
    LabelSpec("area:agent-team", "006b75", "agent-team 운영과 개발 체계 영역"),
    LabelSpec("source_type:human-request", "c5def5", "사람 요청에서 발생한 backlog"),
    LabelSpec("source_type:agent-team", "bfdadc", "agent-team 운영 중 발생한 backlog"),
    LabelSpec("source_type:runtime-observation", "f9d0c4", "실행 관찰과 실패에서 발생한 backlog"),
    LabelSpec("source_type:wbs-planned", "d4c5f9", "WBS 계획에서 issue로 발행된 backlog"),
)
