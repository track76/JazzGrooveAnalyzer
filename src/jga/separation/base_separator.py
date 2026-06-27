"""
=========================================================
Jazz Groove Analyzer (JGA)

Base Separator Interface

Author:
    Angelo Tracanna
=========================================================
"""

from abc import ABC, abstractmethod

from jga.runtime.analysis_context import AnalysisContext


class BaseSeparator(ABC):
    """
    Abstract interface for all source separators.
    """

    @abstractmethod
    def separate(
        self,
        context: AnalysisContext
    ) -> AnalysisContext:
        pass