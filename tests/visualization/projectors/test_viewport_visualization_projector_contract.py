"""
Viewport Visualization Projector Contract.

M43.2

Projects one ScientificVisualizationScene into
another ScientificVisualizationScene according
to one VisualizationViewport.

The projector belongs exclusively to the
Visualization Layer.

It never modifies scientific meaning.
"""

import pytest

from jga.visualization.projectors.viewport_visualization_projector import (
    ViewportVisualizationProjector,
)
from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
)
from jga.visualization.scientific_visualization_viewport import (
    ScientificVisualizationViewport,
)


def test_projector_defines_scene_to_scene_contract():

    projector = ViewportVisualizationProjector()

    scene = ScientificVisualizationScene()

    viewport = ScientificVisualizationViewport(
        x_min=0.0,
        x_max=100.0,
        y_min=-10.0,
        y_max=10.0,
    )

    with pytest.raises(NotImplementedError):
        projector.project(
            scene,
            viewport,
        )


def test_projector_returns_scene():

    scene = ScientificVisualizationScene()

    assert isinstance(
        scene,
        ScientificVisualizationScene,
    )
