from jga.domain.behaviour_change_event import (
    BehaviourChangeEvent,
)

from jga.domain.behaviour_observation_frame import (
    BehaviourObservationFrame,
)

from jga.observation.behaviour_comparator import (
    BehaviourComparator,
)


class StableRegionDetector:

    def __init__(self):

        self.comparator = BehaviourComparator()

    def detect(
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

        start = frames[0]

        previous = start

        events = []

        for current in frames[1:]:

            comparison = self.comparator.compare(
                previous,
                current,
            )

            if not comparison.overall_match:

                events.append(

                    BehaviourChangeEvent(

                        start_time=start.time,

                        end_time=previous.time,

                        event_type="stable_region",

                        intensity=0.0,

                    )

                )

                start = current

            previous = current

        events.append(

            BehaviourChangeEvent(

                start_time=start.time,

                end_time=previous.time,

                event_type="stable_region",

                intensity=0.0,

            )

        )

        return tuple(events)

