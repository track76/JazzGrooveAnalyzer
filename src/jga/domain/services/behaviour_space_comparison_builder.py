from __future__ import annotations

from jga.domain.behaviour_space_comparison import (
    BehaviourSpaceComparison,
)

from jga.geometry.scientific_behaviour_space import (
    ScientificBehaviourSpace,
)


class BehaviourSpaceComparisonBuilder:
    """
    Builds BehaviourSpaceComparison objects.

    Current implementation only validates
    structural comparability.

    No distance or similarity computation
    is performed.
    """

    def build(
        self,
        first: ScientificBehaviourSpace,
        second: ScientificBehaviourSpace,
    ) -> BehaviourSpaceComparison:

        comparable = (
            first.trajectory_count
            ==
            second.trajectory_count
        )

        reason = (
            "Compatible trajectory structure"
            if comparable
            else
            "Different trajectory structure"
        )

        return BehaviourSpaceComparison(
            comparable=comparable,
            reason=reason,
        )
