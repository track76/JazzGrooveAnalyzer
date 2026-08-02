"""
Viewport Projector Adapter.

Adapts DefaultViewportVisualizationProjector
to the VisualizationProjectionPipeline contract.
"""

from jga.visualization.projectors.default_viewport_visualization_projector import (
    DefaultViewportVisualizationProjector,
)
from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
)
from jga.visualization.scientific_visualization_viewport import (
    ScientificVisualizationViewport,
)


class ViewportProjectorAdapter:
    """
    Pipeline-compatible viewport projector.
    """

    def __init__(
        self,
        viewport: ScientificVisualizationViewport,
    ) -> None:

        self._viewport = viewport
        self._projector = (
            DefaultViewportVisualizationProjector()
        )

    def project(
        self,
        scene: ScientificVisualizationScene,
    ) -> ScientificVisualizationScene:

        return self._projector.project(
            scene,
            self._viewport,
        )
