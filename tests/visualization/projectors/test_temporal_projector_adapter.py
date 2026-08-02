from jga.visualization.projectors.temporal_projector_adapter import (
    TemporalProjectorAdapter,
)
from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
)
from jga.visualization.temporal_visualization_window import (
    TemporalVisualizationWindow,
)


def test_temporal_adapter_preserves_contract():

    adapter = TemporalProjectorAdapter(
        window=TemporalVisualizationWindow(
            start_time=0.0,
            end_time=1.0,
        ),
    )

    result = adapter.project(
        ScientificVisualizationScene(),
    )

    assert isinstance(
        result,
        ScientificVisualizationScene,
    )
