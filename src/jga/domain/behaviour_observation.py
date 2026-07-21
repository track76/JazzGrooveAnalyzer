from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from jga.domain.internal_metric_timeline import InternalMetricTimeline
from jga.domain.pulse import Pulse


@dataclass(frozen=True, slots=True)
class BehaviourObservation:
    """
    Smallest behavioural observation extracted from a validated
    InternalMetricTimeline.
    """

    id: UUID
    timeline: InternalMetricTimeline
    first_pulse: Pulse
    last_pulse: Pulse
    created_at: datetime

    def __post_init__(self) -> None:
        if self.first_pulse.index > self.last_pulse.index:
            raise ValueError(
                "first_pulse must not follow last_pulse"
            )
