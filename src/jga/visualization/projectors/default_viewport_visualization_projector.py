"""
Default Viewport Visualization Projector.

Projects one ScientificVisualizationScene into
another by filtering visual points inside one
ScientificVisualizationViewport.

The operation belongs exclusively to the
Visualization Layer.
"""

from jga.visualization.projectors.viewport_visualization_projector import (
    ViewportVisualizationProjector,
)
from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
)
from jga.visualization.scientific_visualization_viewport import (
    ScientificVisualizationViewport,
)
from jga.visualization.visual_point import (
    VisualPoint,
)
from jga.visualization.visual_trajectory import (
    VisualTrajectory,
)
from jga.visualization.visualization_trajectory_descriptor import (
    VisualizationTrajectoryDescriptor,
)


class DefaultViewportVisualizationProjector(
    ViewportVisualizationProjector,
):
    """
    Default viewport projector.

    Keeps only the visual points contained
    inside the requested viewport.
    """

    def project(
        self,
        scene: ScientificVisualizationScene,
        viewport: ScientificVisualizationViewport,
    ) -> ScientificVisualizationScene:

        projected_trajectories = []

        for descriptor in scene.trajectories:

            points = tuple(
                point
                for point in descriptor.trajectory.points
                if (
                    viewport.x_min <= point.x <= viewport.x_max
                    and
                    viewport.y_min <= point.y <= viewport.y_max
                )
            )

            projected_trajectories.append(
                VisualizationTrajectoryDescriptor(
                    identifier=descriptor.identifier,
                    trajectory=VisualTrajectory(
                        points=points,
                    ),
                )
            )

        return ScientificVisualizationScene(
            trajectories=tuple(
                projected_trajectories
            ),
        )
