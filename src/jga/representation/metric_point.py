"""
Metric Point.

Elementary geometric representation of one
Elementary Metric Event.

Scientific references:

- G-001 Metric Geometry
- G-002 Metric Cluster Geometry
- G-004 Metric Cluster Portrait Geometry
"""

from dataclasses import dataclass

from jga.domain.elementary_metric_event import ElementaryMetricEvent


@dataclass(frozen=True, slots=True)
class MetricPoint:
    """
    Immutable geometric projection of one
    Elementary Metric Event.
    """

    event: ElementaryMetricEvent

    offset_ms: float
