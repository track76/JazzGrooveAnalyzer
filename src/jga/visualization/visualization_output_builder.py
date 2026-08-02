"""
Visualization Output Builder.

Creates visualization output artifacts
from scientific visualization scenes.
"""

from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
)

from jga.visualization.visualization_output import (
    VisualizationOutput,
)


class VisualizationOutputBuilder:
    """
    Builds visualization outputs.
    """

    def build(
        self,
        scene: ScientificVisualizationScene,
    ) -> VisualizationOutput:

        return VisualizationOutput(
            scene=scene,
            description=(
                "Scientific visualization output"
            ),
            metadata={
                "trajectory_count": len(
                    scene.trajectories,
                ),
                "annotation_count": len(
                    scene.annotations,
                ),
            },
        )
