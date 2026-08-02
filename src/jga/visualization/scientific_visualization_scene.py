"""
Scientific Visualization Scene.

Visualization Layer container for multiple
identified visual trajectories.
"""

from dataclasses import dataclass

from jga.visualization.visualization_trajectory_descriptor import (
    VisualizationTrajectoryDescriptor,
)


@dataclass(frozen=True, slots=True)
class ScientificVisualizationScene:
    """
    Immutable visualization scene.

    Contains identified visual trajectories.
    """

    trajectories: tuple[
        VisualizationTrajectoryDescriptor,
        ...
    ] = ()
