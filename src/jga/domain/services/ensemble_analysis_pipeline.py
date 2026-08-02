from __future__ import annotations

from abc import ABC, abstractmethod

from jga.domain.ensemble_analysis_result import (
    EnsembleAnalysisResult,
)
from jga.domain.sound_source import SoundSource


class EnsembleAnalysisPipeline(ABC):
    """
    Performs semantic ensemble analysis starting from
    already identified Domain sound sources.

    Input:
        tuple[SoundSource, ...]

    Output:
        EnsembleAnalysisResult
    """

    @abstractmethod
    def analyze(
        self,
        sound_sources: tuple[SoundSource, ...],
    ) -> EnsembleAnalysisResult:
        ...
