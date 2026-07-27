from jga.domain.behaviour_change_event import (
    BehaviourChangeEvent,
)

from jga.domain.behaviour_observation_frame import (
    BehaviourObservationFrame,
)

from jga.observation.stable_region_detector import (
    StableRegionDetector,
)


class DefaultBehaviourDiagnostics:
    """
    Behaviour Diagnostics coordinator.

    Each detector analyses one specific
    behavioural phenomenon.
    """

    def __init__(self):

        self._stable_detector = (
            StableRegionDetector()
        )

    def analyze(
        self,
        frames: tuple[
            BehaviourObservationFrame,
            ...
        ],
    ) -> tuple[
        BehaviourChangeEvent,
        ...
    ]:

        return self._stable_detector.detect(
            frames,
        )
