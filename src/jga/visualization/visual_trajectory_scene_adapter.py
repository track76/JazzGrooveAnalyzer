"""
Visual Trajectory Scene Adapter.

Converts one VisualTrajectory into one
ScientificVisualizationScene.
"""

from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
)

from jga.visualization.visual_trajectory import (
    VisualTrajectory,
)

from jga.visualization.visualization_trajectory_descriptor import (
    VisualizationTrajectoryDescriptor,
)


class VisualTrajectorySceneAdapter:
    """
    Adapts one VisualTrajectory into one
    ScientificVisualizationScene.
    """

    def adapt(
        self,
        trajectory: VisualTrajectory,
        identifier: str,
    ) -> ScientificVisualizationScene:

        return ScientificVisualizationScene(
            trajectories=(
                VisualizationTrajectoryDescriptor(
                    identifier=identifier,
                    trajectory=trajectory,
                ),
            ),
        )
