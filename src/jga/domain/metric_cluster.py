from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from jga.domain.beat_reference import BeatReference
from jga.domain.elementary_metric_event import ElementaryMetricEvent


@dataclass(frozen=True, slots=True)
class MetricCluster:
    """
    Reconstructed metric movement.

    A MetricCluster represents one BeatReference inside the
    reconstructed metric timeline.

    It may contain zero or more ElementaryMetricEvents.
    Events are observations of real audio contributors and are
    not artificially generated.
    """

    id: UUID
    beat_reference: BeatReference
    events: tuple[ElementaryMetricEvent, ...]
    created_at: datetime

    @property
    def size(self) -> int:
        return len(self.events)
