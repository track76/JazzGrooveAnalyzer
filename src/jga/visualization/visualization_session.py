"""
Visualization Session.

Manages the current visualization state.

The session belongs exclusively to the
Visualization Layer.

It does not modify scientific data.
"""

from __future__ import annotations

from dataclasses import dataclass, replace

from jga.visualization.visualization_state import (
    VisualizationState,
)

from jga.visualization.pipeline.visualization_projection_pipeline import (
    VisualizationProjectionPipeline,
)


@dataclass(frozen=True, slots=True)
class VisualizationSession:
    """
    Holds the current visualization state.
    """

    state: VisualizationState

    projection_pipeline: object | None = None

    history: tuple[
        VisualizationState,
        ...
    ] = ()

    def __post_init__(self):
        if not self.history:
            object.__setattr__(
                self,
                "history",
                (
                    self.state,
                ),
            )


    def project(
        self,
        scene,
    ):
        """
        Projects a scene using the current
        visualization state.
        """

        pipeline = (
            self.projection_pipeline
            if self.projection_pipeline is not None
            else VisualizationProjectionPipeline()
        )

        return pipeline.project(
            scene,
            state=self.state,
        )

    def update_state(
        self,
        **changes,
    ) -> "VisualizationSession":
        """
        Returns a new session with an updated state.

        The current session remains unchanged.
        """

        new_state = replace(
            self.state,
            **changes,
        )

        return VisualizationSession(
            state=new_state,
            projection_pipeline=self.projection_pipeline,
            history=(
                *self.history,
                new_state,
            ),
        )
