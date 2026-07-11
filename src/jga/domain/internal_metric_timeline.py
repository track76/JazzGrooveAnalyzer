from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from jga.domain.pulse import Pulse


@dataclass(frozen=True, slots=True)
class InternalMetricTimeline:
    """
    Represents the Internal Metric Timeline (IMT) of a musical performance.

    The Internal Metric Timeline is the ordered sequence of inferred Pulse
    instances that constitutes the temporal reference of the ensemble.

    It is not directly observable.
    It is inferred from the Pulse sequence.
    """

    id: UUID
    pulses: tuple[Pulse, ...]
    created_at: datetime

    def __post_init__(self) -> None:
        if len(self.pulses) == 0:
            raise ValueError(
                "InternalMetricTimeline must contain at least one Pulse"
            )

    @property
    def pulse_count(self) -> int:
        return len(self.pulses)

    @property
    def first_pulse(self) -> Pulse:
        return self.pulses[0]

    @property
    def last_pulse(self) -> Pulse:
        return self.pulses[-1]