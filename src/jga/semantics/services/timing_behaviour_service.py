"""
Timing Behaviour Service.
"""

from jga.semantics.observations.metric_event_observation import (
    MetricEventObservation,
)
from jga.semantics.timing_behaviour import (
    TimingBehaviour,
)


class TimingBehaviourService:
    """
    Determines Timing Behaviour from observable data.

    Current implementation intentionally returns
    UNKNOWN until scientific rules are defined.
    """

    def classify(
        self,
        observation: MetricEventObservation,
    ) -> TimingBehaviour:

        _ = observation

        return TimingBehaviour.UNKNOWN
