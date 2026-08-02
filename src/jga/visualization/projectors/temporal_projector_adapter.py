"""
Temporal Projector Adapter.

Adapts DefaultTemporalVisualizationProjector
to the VisualizationProjectionPipeline contract.
"""

from jga.visualization.projectors.default_temporal_visualization_projector import (
    DefaultTemporalVisualizationProjector,
)
from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
)
from jga.visualization.temporal_visualization_window import (
    TemporalVisualizationWindow,
)


class TemporalProjectorAdapter:
    """
    Pipeline-compatible temporal projector.
    """

    def __init__(
        self,
        window: TemporalVisualizationWindow,
    ) -> None:

        self._window = window
        self._projector = (
            DefaultTemporalVisualizationProjector()
        )

    def project(
        self,
        scene: ScientificVisualizationScene,
    ) -> ScientificVisualizationScene:

        return self._projector.project(
            scene,
            self._window,
        )
