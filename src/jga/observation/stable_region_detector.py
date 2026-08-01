from jga.domain.behaviour_change_event import (
    BehaviourChangeEvent,
)
from jga.domain.behaviour_observation_frame import (
    BehaviourObservationFrame,
)

from jga.domain.stable_region_detection_result import (
    StableRegionDetectionResult,
)

from jga.observation.behaviour_comparator import (
    BehaviourComparator,
)
from jga.observation.builders.behaviour_state_builder import (
    BehaviourStateBuilder,
)


class StableRegionDetector:

    def __init__(self):

        self.comparator = BehaviourComparator()

        self.state_builder = (
            BehaviourStateBuilder()
        )


    def detect(
        self,
        frames: tuple[
            BehaviourObservationFrame,
            ...
        ],
    ) -> StableRegionDetectionResult:

        if not frames:
            return StableRegionDetectionResult(
                events=(),
                evidences=(),
            )

        start = 0

        previous = 0

        events = []
        evidences = []

        for current in range(1, len(frames)):

            comparison = self.comparator.compare(
                frames[previous],
                frames[current],
            )

            evidences.append(
                self.comparator.compare_with_evidence(
                    frames[previous],
                    frames[current],
                )
            )

            if not comparison.overall_match:

                state = self.state_builder.build(
                    frames=frames,
                    start_index=start,
                    end_index=previous,
                )

                events.append(

                    BehaviourChangeEvent(

                        start_time=frames[state.start_index].time,

                        end_time=frames[state.end_index].time,

                        event_type="stable_region",

                        intensity=0.0,

                    )

                )

                start = current

            previous = current

        state = self.state_builder.build(
            frames=frames,
            start_index=start,
            end_index=previous,
        )

        events.append(

            BehaviourChangeEvent(

                start_time=frames[state.start_index].time,

                end_time=frames[state.end_index].time,

                event_type="stable_region",

                intensity=0.0,

            )

        )

        return StableRegionDetectionResult(
            events=tuple(events),
            evidences=tuple(evidences),
        )

