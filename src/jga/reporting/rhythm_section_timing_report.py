"""Canonical analyst-facing export for the AD-040 timing profile."""

from dataclasses import dataclass
from pathlib import Path
from typing import Literal


AnalyticalRole = Literal["TEMPORAL_REFERENCE", "ACCOMPANIMENT"]


class RhythmSectionTimingReportError(ValueError):
    """A bounded failure in report authority, construction, or export."""


@dataclass(frozen=True, slots=True)
class AuthorizedSourceInput:
    """Caller-supplied source and analytical-role authority."""

    path: Path
    label: str
    role: AnalyticalRole
    expected_sha256: str | None = None


@dataclass(frozen=True, slots=True)
class RhythmSectionTimingReport:
    """Immutable canonical JSON report content."""

    schema_id: str
    schema_version: int
    scientific_fingerprint: str
    canonical_json: str

    def write(self, destination: Path) -> None:
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("x", encoding="utf-8", newline="\n") as output:
            output.write(self.canonical_json)
