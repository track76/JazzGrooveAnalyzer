from __future__ import annotations

from abc import ABC, abstractmethod

from jga.core.domain.audio_stem import AudioStem
from jga.core.domain.ensemble_analysis_result import (
    EnsembleAnalysisResult,
)


class EnsembleAnalysisPipeline(ABC):

    @abstractmethod
    def analyze(
        self,
        stems: tuple[AudioStem, ...],
    ) -> EnsembleAnalysisResult:
        ...