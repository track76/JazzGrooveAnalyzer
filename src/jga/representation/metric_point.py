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

from jga.domain.elementary_metric_event import (
    ElementaryMetricEvent,
)

from jga.domain.beat_reference import (
    BeatReference,
)

from jga.representation.scientific_coordinate import (
    ScientificCoordinate,
)


@dataclass(frozen=True, slots=True)
class MetricPoint:
    """
    Immutable geometric projection of one
    Elementary Metric Event.
    """

    event: ElementaryMetricEvent

    coordinate: ScientificCoordinate

    beat_reference: BeatReference | None = None

    beat_index: int = 0

    @property
    def offset_ms(self) -> float:
        """
        Backward compatible access to temporal displacement.
        """

        return self.coordinate.value

    @property
    def offset_seconds(self) -> float:
        """Neutral signed temporal displacement in physical seconds."""

        return self.coordinate.value / 1000.0
