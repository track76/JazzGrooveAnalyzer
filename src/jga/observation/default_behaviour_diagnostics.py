from jga.domain.behaviour_change_event import (
    BehaviourChangeEvent,
)

from jga.domain.behaviour_observation_frame import (
    BehaviourObservationFrame,
)


class DefaultBehaviourDiagnostics:
    """
    First implementation of Behaviour Diagnostics.

    Current version returns one stable event.

    Future versions will detect behavioural
    transitions.
    """

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

        if not frames:
            return ()

        return (

            BehaviourChangeEvent(

                start_time=frames[0].time,

                end_time=frames[-1].time,

                event_type="stable",

                intensity=0.0,

            ),

        )
