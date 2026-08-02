"""
Visualization Trajectory Descriptor.

Visualization Layer metadata container.
"""

from dataclasses import dataclass

from jga.visualization.visual_trajectory import (
    VisualTrajectory,
)


@dataclass(frozen=True, slots=True)
class VisualizationTrajectoryDescriptor:
    """
    Identifies a visual trajectory.

    Contains only visualization metadata.
    """

    identifier: str

    trajectory: VisualTrajectory
