from __future__ import annotations

from dataclasses import dataclass

from jga.source_understanding.observed_source import (
    ObservedSource,
)


@dataclass(frozen=True, slots=True)
class SourceUnderstandingResult:
    """
    Semantic understanding of the observed sound sources.
    """

    observed_sources: tuple[ObservedSource, ...]
