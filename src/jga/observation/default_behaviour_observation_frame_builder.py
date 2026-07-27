from jga.domain.behaviour_observation_frame import (
    BehaviourObservationFrame,
)

from jga.geometry.scientific_behaviour_space import (
    ScientificBehaviourSpace,
)


class DefaultBehaviourObservationFrameBuilder:
    """
    Builds Behaviour Observation Frames from a
    Scientific Behaviour Space.

    This component performs no scientific
    interpretation.
    """

    def build(
        self,
        behaviour_space: ScientificBehaviourSpace,
    ) -> tuple[
        BehaviourObservationFrame,
        ...
    ]:

        frames = []

        for trajectory in behaviour_space:

            for index, point in enumerate(trajectory):

                frames.append(

                    BehaviourObservationFrame(

                        time=float(index),

                        physical_offset_ms=0.0,

                        metric_offset=0.0,

                        internal_bpm=0.0,

                        stability=0.0,

                    )

                )

        return tuple(frames)
