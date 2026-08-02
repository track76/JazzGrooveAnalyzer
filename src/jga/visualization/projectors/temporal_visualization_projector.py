from __future__ import annotations

from abc import ABC, abstractmethod

from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
)
from jga.visualization.temporal_visualization_window import (
    TemporalVisualizationWindow,
)


class TemporalVisualizationProjector(ABC):
    """
    Projects a ScientificVisualizationScene into a temporal window.

    This transformation belongs entirely to the Visualization Layer.

    It performs no scientific interpretation and does not modify the
    meaning of the represented data.

    Input:
        - ScientificVisualizationScene
        - TemporalVisualizationWindow

    Output:
        - ScientificVisualizationScene
    """

    @abstractmethod
    def project(
        self,
        scene: ScientificVisualizationScene,
        window: TemporalVisualizationWindow,
    ) -> ScientificVisualizationScene:
        """
        Returns a new scene containing only the visualization data
        belonging to the requested temporal window.
        """
        raise NotImplementedError
