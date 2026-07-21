from datetime import datetime
from uuid import uuid4

from jga.domain.behaviour_observation import BehaviourObservation
from jga.domain.internal_metric_timeline import InternalMetricTimeline


class BehaviourObservationBuilder:
    """
    Builds one BehaviourObservation from one InternalMetricTimeline.
    """

    def build(
        self,
        timeline: InternalMetricTimeline,
    ) -> BehaviourObservation:

        return BehaviourObservation(
            id=uuid4(),
            timeline=timeline,
            first_pulse=timeline.first_pulse,
            last_pulse=timeline.last_pulse,
            created_at=datetime.now(),
        )
