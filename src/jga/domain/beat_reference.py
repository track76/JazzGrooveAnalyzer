from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True, slots=True)
class BeatReference:
    """
    Represents one theoretical beat of the ensemble metric grid.

    A BeatReference is not directly observed.

    It is inferred from the recognised metric structure and
    acts as the temporal reference used to associate
    ElementaryMetricEvents to MetricClusters.
    """

    id: UUID

    index: int

    timestamp: float

    created_at: datetime

    def __post_init__(self):

        if self.index < 0:
            raise ValueError(
                "index must be non-negative"
            )

        if self.timestamp < 0.0:
            raise ValueError(
                "timestamp must be non-negative"
            )