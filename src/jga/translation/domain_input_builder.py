"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    domain_input_builder.py

Description:
    Default implementation of the mathematical
    transformation τ₈ (Representation Translation).

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from jga.interfaces.translation.domain_input_builder import (
    DomainInputBuilder,
)

from jga.runtime.analysis_context import AnalysisContext
from jga.translation.tau8_translator import Tau8Translator


class DefaultDomainInputBuilder(DomainInputBuilder):
    """
    Default implementation of τ₈.

    Performs the deterministic representation
    translation from MetricContext to
    ElementaryMetricEvent domain entities.

    No musical interpretation is introduced.
    """

    def __init__(self):

        self.tau8 = Tau8Translator()

    def build(
        self,
        context: AnalysisContext,
    ) -> AnalysisContext:

        if context is None:
            raise ValueError(
                "AnalysisContext cannot be None."
            )

        if context.metric_context is None:
            raise ValueError(
                "MetricContext required for τ₈ translation."
            )

        context.elementary_metric_events = (
            self.tau8.translate(
                context.metric_context
            )
        )

        return context
