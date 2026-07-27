from jga.observation.default_behaviour_observation_frame_builder import (
    DefaultBehaviourObservationFrameBuilder,
)

from jga.observation.default_behaviour_diagnostics import (
    DefaultBehaviourDiagnostics,
)

from jga.runtime.analysis_context import AnalysisContext


class BehaviourObservationRunner:
    """
    Runtime adapter connecting the Scientific Behaviour
    Space with the Observation Layer.
    """

    def __init__(self) -> None:

        self._builder = (
            DefaultBehaviourObservationFrameBuilder()
        )

        self._diagnostics = (
            DefaultBehaviourDiagnostics()
        )

    def run(
        self,
        context: AnalysisContext,
    ) -> None:

        if context.scientific_behaviour_space is None:
            return

        frames = self._builder.build(
            context.scientific_behaviour_space,
        )

        context.behaviour_observation_frames = (
            frames
        )

        context.behaviour_change_events = (
            self._diagnostics.analyze(
                frames,
            )
        )
