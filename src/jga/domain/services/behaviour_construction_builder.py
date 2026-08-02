
from jga.domain.behaviour_construction_result import (
    BehaviourConstructionResult,
)

from jga.domain.internal_metric_timeline import (
    InternalMetricTimeline,
)

from jga.domain.services.behaviour_observation_builder import (
    BehaviourObservationBuilder,
)

from jga.domain.services.behaviour_profile_builder import (
    BehaviourProfileBuilder,
)


class BehaviourConstructionBuilder:
    """
    Orchestrates Behaviour construction.

    Pipeline:

        InternalMetricTimeline
                ↓
        BehaviourObservationBuilder
                ↓
        BehaviourProfileBuilder
                ↓
        BehaviourConstructionResult
    """

    def __init__(self) -> None:

        self._observation_builder = (
            BehaviourObservationBuilder()
        )

        self._profile_builder = (
            BehaviourProfileBuilder()
        )

    def build(
        self,
        timeline: InternalMetricTimeline,
    ) -> BehaviourConstructionResult:

        observations = (
            self._observation_builder.build(
                timeline,
            )
        )

        if not observations:
            return BehaviourConstructionResult(
                behaviour_observations=(),
                behaviour_profile=None,
            )

        profile = (
            self._profile_builder.build(
                observations,
            )
        )

        return BehaviourConstructionResult(
            behaviour_observations=observations,
            behaviour_profile=profile,
        )
