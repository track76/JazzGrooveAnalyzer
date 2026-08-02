"""
Graphical Renderer Contract.

Visualization Layer rendering boundary.
"""

from abc import ABC, abstractmethod

from jga.visualization.visual_trajectory import (
    VisualTrajectory,
)


class GraphicalRenderer(ABC):
    """
    Abstract graphical renderer.
    """

    @abstractmethod
    def render(
        self,
        trajectory: VisualTrajectory,
    ):
        """
        Render a visual trajectory.
        """
        raise NotImplementedError
