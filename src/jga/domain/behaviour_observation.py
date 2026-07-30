from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from jga.domain.internal_metric_timeline import InternalMetricTimeline
from jga.domain.pulse import Pulse


@dataclass(slots=True, frozen=True)
class BehaviourObservation:
    """
    Observation of a behaviour over a portion of the reconstructed
    Internal Metric Timeline.
    """

    id: UUID
    timeline: InternalMetricTimeline
    first_pulse: Pulse
    last_pulse: Pulse
    created_at: datetime
