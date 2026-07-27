from jga.domain.behaviour_observation_frame import (
    BehaviourObservationFrame,
)

from jga.observation.diagnostic_thresholds import (
    DiagnosticThresholds,
)


class PhysicalOffsetComparator:
    """
    Compares the physical metric offset of two
    Behaviour Observation Frames.
    """

    def __init__(self):

        self.thresholds = DiagnosticThresholds()

    def compare(
        self,
        left: BehaviourObservationFrame,
        right: BehaviourObservationFrame,
    ) -> bool:

        return abs(

            left.physical_offset_ms
            - right.physical_offset_ms

        ) <= self.thresholds.physical_offset_ms

