from uuid import uuid4

from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
)

from jga.visualization.temporal_visualization_window import (
    TemporalVisualizationWindow,
)

from jga.visualization.visualization_annotation import (
    VisualizationAnnotation,
)


def test_scene_returns_none_when_reference_is_outside_window():

    reference = uuid4()

    scene = ScientificVisualizationScene(
        annotations=(
            VisualizationAnnotation(
                timestamp=50.0,
                label="metric_event",
                reference_id=reference,
            ),
        ),
    )

    window = TemporalVisualizationWindow(
        start_time=10.0,
        end_time=30.0,
    )

    result = scene.annotation_for_reference_in_window(
        reference,
        window,
    )

    assert result is None
