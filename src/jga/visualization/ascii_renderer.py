"""
ASCII Renderer.

First Visualization Layer renderer.
"""

from jga.visualization.visual_trajectory import (
    VisualTrajectory,
)


class ASCIIRenderer:
    """
    Renders visual trajectories into
    textual representation.
    """

    def render(
        self,
        trajectory: VisualTrajectory,
    ) -> str:
        """
        Produces a deterministic textual output.
        """

        lines = []

        for point in trajectory.points:
            lines.append(
                f"({point.x},{point.y})"
            )

        return "\n".join(lines)
