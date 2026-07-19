"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    tau8_translator.py

Description:
    Implementation boundary of mathematical
    transformation τ₈.

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from jga.core.metric_context import MetricContext
from jga.domain.elementary_metric_event import ElementaryMetricEvent


class Tau8Translator:
    """
    Software boundary implementing τ₈.

    τ₈ transforms the observable Metric Context
    into Domain ElementaryMetricEvent representations.

    The transformation is representational only.

    It does not:
    - modify observations;
    - quantize timestamps;
    - interpolate events;
    - introduce musical interpretation.
    """

    def translate(
        self,
        metric_context: MetricContext,
    ) -> tuple[ElementaryMetricEvent, ...]:

        raise NotImplementedError(
            "τ₈ translation is not implemented yet."
        )
