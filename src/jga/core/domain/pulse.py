from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from jga.core.domain.metric_cluster import MetricCluster


@dataclass(frozen=True, slots=True)
class Pulse:
    """
    Represents one inferred occurrence of the ensemble pulse.

    A Pulse is estimated from exactly one MetricCluster.
    It is not a directly observable musical event.
    """

    id: UUID
    index: int
    cluster: MetricCluster
    timestamp: float
    created_at: datetime

    def __post_init__(self) -> None:
        if self.index < 0:
            raise ValueError("index must be non-negative")

        if self.timestamp < 0.0:
            raise ValueError("timestamp must be non-negative")