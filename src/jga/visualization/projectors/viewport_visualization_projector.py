"""
Viewport Visualization Projector.

Defines the contract for visualization
projectors operating on one visualization
viewport.

The projector belongs exclusively to the
Visualization Layer.
"""

from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
)
from jga.visualization.scientific_visualization_viewport import (
    ScientificVisualizationViewport,
)


class ViewportVisualizationProjector:
    """
    Projects one ScientificVisualizationScene
    into another according to one viewport.

    This operation never modifies scientific
    meaning.
    """

    def project(
        self,
        scene: ScientificVisualizationScene,
        viewport: ScientificVisualizationViewport,
    ) -> ScientificVisualizationScene:
        """
        Projects one visualization scene into
        the requested viewport.

        Subclasses must implement this method.
        """

        raise NotImplementedError
