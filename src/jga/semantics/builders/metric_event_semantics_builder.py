"""
Metric Event Semantics Builder.
"""

from jga.semantics.metric_event_semantics import (
    MetricEventSemantics,
)


class MetricEventSemanticsBuilder:
    """
    Builds semantic information associated with
    a Metric Event.

    Current implementation intentionally returns the
    neutral semantic representation.
    """

    def build(
        self,
    ) -> MetricEventSemantics:

        return MetricEventSemantics()
