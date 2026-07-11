from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from jga.core.domain.beat_reference import BeatReference
from jga.core.domain.elementary_metric_event import ElementaryMetricEvent


@dataclass(frozen=True, slots=True)
class MetricCluster:
    """
    First inferred temporal structure of the Jazz Groove Analyzer.

    A MetricCluster groups one or more ElementaryMetricEvents that
    collectively represent a single metric occurrence.

    It is inferred, not directly observed.
    """

    id: UUID
    beat_reference: BeatReference
    events: tuple[ElementaryMetricEvent, ...]
    created_at: datetime

    def __post_init__(self) -> None:
        if len(self.events) == 0:
            raise ValueError(
                "MetricCluster must contain at least one ElementaryMetricEvent"
            )

    @property
    def size(self) -> int:
        return len(self.events)