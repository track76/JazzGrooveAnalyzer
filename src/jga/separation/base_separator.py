"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    base_separator.py

Description:
    Abstract interface for every audio separator.

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from abc import ABC
from abc import abstractmethod

from jga.runtime.analysis_context import AnalysisContext


class BaseSeparator(ABC):
    """
    Base class for every source separation engine.
    """

    @abstractmethod
    def process(
        self,
        context: AnalysisContext
    ) -> AnalysisContext:
        """
        Produces one or more AudioStem objects.

        Returns
        -------
        AnalysisContext
        """
        pass