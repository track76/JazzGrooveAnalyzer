from jga.domain.behaviour_comparison_result import (
    BehaviourComparisonResult,
)

from jga.domain.behaviour_observation_frame import (
    BehaviourObservationFrame,
)

from jga.observation.comparators.physical_offset_comparator import (
    PhysicalOffsetComparator,
)


class BehaviourComparator:
    """
    Aggregates scientific comparisons.
    """

    def __init__(self):

        self._physical = (
            PhysicalOffsetComparator()
        )

    def compare(
        self,
        left: BehaviourObservationFrame,
        right: BehaviourObservationFrame,
    ) -> BehaviourComparisonResult:

        physical = self._physical.compare(
            left,
            right,
        )

        return BehaviourComparisonResult(

            physical_offset_match=physical,

            metric_offset_match=True,

            internal_bpm_match=True,

            stability_match=True,

        )

