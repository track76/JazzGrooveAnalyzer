"""
Visualization Projection Pipeline.

Applies one or more visualization projectors
to a ScientificVisualizationScene.

This pipeline belongs exclusively to the
Visualization Layer.

It performs no scientific interpretation.
"""

from __future__ import annotations

from dataclasses import dataclass

from jga.visualization.projectors.temporal_visualization_projector import (
    TemporalVisualizationProjector,
)
from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
)

from jga.visualization.temporal_visualization_window import (
    TemporalVisualizationWindow,
)

from jga.visualization.visualization_state import (
    VisualizationState,
)


@dataclass(frozen=True, slots=True)
class VisualizationProjectionPipeline:
    """
    Sequentially applies visualization
    projectors to a scene.
    """

    projectors: tuple[
        TemporalVisualizationProjector,
        ...
    ] = ()

    def project(
        self,
        scene: ScientificVisualizationScene,
        window: TemporalVisualizationWindow | None = None,
        *,
        state: VisualizationState | None = None,
    ) -> ScientificVisualizationScene:
        """
        Applies an optional temporal window
        and all configured projectors.
        """

        current_scene = scene

        if (
            state is not None
            and state.selected_sources
        ):
            current_scene = current_scene.filter(
                *state.selected_sources,
            )

        if (
            state is not None
            and state.active_annotations
        ):
            current_scene = ScientificVisualizationScene(
                trajectories=current_scene.trajectories,
                annotations=state.active_annotations,
            )

        if window is not None:
            current_scene = current_scene.slice(
                window,
            )

        elif (
            state is not None
            and state.temporal_window is not None
        ):
            current_scene = current_scene.slice(
                state.temporal_window,
            )

        for projector in self.projectors:
            current_scene = projector.project(
                current_scene,
            )

        return current_scene
