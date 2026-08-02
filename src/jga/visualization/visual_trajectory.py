"""
Visual Trajectory.

Visualization Layer graphical path.
"""

from dataclasses import dataclass

from jga.visualization.visual_point import (
    VisualPoint,
)


@dataclass(frozen=True, slots=True)
class VisualTrajectory:
    """
    Immutable graphical trajectory.

    Contains only visual points.
    """

    points: tuple[VisualPoint, ...] = ()
