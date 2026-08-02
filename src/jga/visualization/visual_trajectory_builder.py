"""
Visual Trajectory Builder.

Visualization Layer builder for graphical paths.
"""

from jga.visualization.visual_point import (
    VisualPoint,
)

from jga.visualization.visual_trajectory import (
    VisualTrajectory,
)


class VisualTrajectoryBuilder:
    """
    Builds immutable visual trajectories.
    """

    def build(
        self,
        points: tuple[VisualPoint, ...],
    ) -> VisualTrajectory:
        """
        Creates a visual trajectory from
        ordered visual points.
        """

        return VisualTrajectory(
            points=points,
        )
