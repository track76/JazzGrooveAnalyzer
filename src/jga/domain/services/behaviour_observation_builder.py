from datetime import datetime
from uuid import uuid4

from jga.domain.behaviour_observation import BehaviourObservation
from jga.domain.internal_metric_timeline import InternalMetricTimeline


class BehaviourObservationBuilder:
    """
    Builds BehaviourObservation objects from an InternalMetricTimeline.
    """

    def build(
        self,
        timeline: InternalMetricTimeline,
    ) -> tuple[BehaviourObservation, ...]:

        return tuple(
            BehaviourObservation(
                id=uuid4(),
                timeline=timeline,
                first_pulse=pulse,
                last_pulse=pulse,
                created_at=datetime.now(),
            )
            for pulse in timeline.pulses
        )
