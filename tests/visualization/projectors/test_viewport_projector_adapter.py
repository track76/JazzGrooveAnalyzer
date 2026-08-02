from jga.visualization.projectors.viewport_projector_adapter import (
    ViewportProjectorAdapter,
)
from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
)
from jga.visualization.scientific_visualization_viewport import (
    ScientificVisualizationViewport,
)


def test_adapter_preserves_project_contract():

    adapter = ViewportProjectorAdapter(
        viewport=ScientificVisualizationViewport(
            x_min=0.0,
            x_max=1.0,
            y_min=0.0,
            y_max=1.0,
        ),
    )

    result = adapter.project(
        ScientificVisualizationScene(),
    )

    assert isinstance(
        result,
        ScientificVisualizationScene,
    )
