"""
Default Temporal Visualization Projector.

Filters visualization data according to a
TemporalVisualizationWindow.

This transformation belongs exclusively
to the Visualization Layer.

It performs no scientific interpretation.
"""

from jga.visualization.projectors.temporal_visualization_projector import (
    TemporalVisualizationProjector,
)
from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
)
from jga.visualization.temporal_visualization_window import (
    TemporalVisualizationWindow,
)
from jga.visualization.visual_trajectory import (
    VisualTrajectory,
)
from jga.visualization.visualization_trajectory_descriptor import (
    VisualizationTrajectoryDescriptor,
)


class DefaultTemporalVisualizationProjector(
    TemporalVisualizationProjector,
):
    """
    Default implementation of the temporal
    visualization projector.
    """

    def project(
        self,
        scene: ScientificVisualizationScene,
        window: TemporalVisualizationWindow,
    ) -> ScientificVisualizationScene:
        """
        Projects one visualization scene into
        the requested temporal window.
        """

        projected_descriptors = []

        for descriptor in scene.trajectories:

            filtered_points = tuple(
                point
                for point in descriptor.trajectory.points
                if window.contains(point.time)
            )

            projected_descriptors.append(
                VisualizationTrajectoryDescriptor(
                    identifier=descriptor.identifier,
                    trajectory=VisualTrajectory(
                        points=filtered_points,
                    ),
                )
            )

        return ScientificVisualizationScene(
            trajectories=tuple(
                projected_descriptors,
            ),
        )
