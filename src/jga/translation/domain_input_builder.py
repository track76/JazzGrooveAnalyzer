"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    domain_input_builder.py
=========================================================
"""

from jga.interfaces.translation.domain_input_builder import (
    DomainInputBuilder,
)
from jga.runtime.analysis_context import AnalysisContext


class DefaultDomainInputBuilder(DomainInputBuilder):
    """
    Default implementation of the Translation Layer.

    At the current stage of the project, the Translation
    Layer establishes the architectural boundary between
    the computational pipeline and the Domain.

    Concrete translation rules will be introduced
    incrementally during Metric Reconstruction.
    """

    def build(
        self,
        context: AnalysisContext,
    ) -> AnalysisContext:
        """
        Returns a validated AnalysisContext ready to be
        consumed by the Domain layer.
        """

        if context is None:
            raise ValueError("AnalysisContext cannot be None.")

        return context
