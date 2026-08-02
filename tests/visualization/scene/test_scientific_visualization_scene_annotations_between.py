from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
)

from jga.visualization.temporal_visualization_window import (
    TemporalVisualizationWindow,
)

from jga.visualization.visualization_annotation import (
    VisualizationAnnotation,
)


def test_scene_queries_annotations_between_window():

    scene = ScientificVisualizationScene(
        annotations=(
            VisualizationAnnotation(
                timestamp=10.0,
                label="a",
            ),
            VisualizationAnnotation(
                timestamp=20.0,
                label="b",
            ),
            VisualizationAnnotation(
                timestamp=40.0,
                label="c",
            ),
        ),
    )

    window = TemporalVisualizationWindow(
        start_time=15.0,
        end_time=25.0,
    )

    result = scene.annotations_between(
        window,
    )

    assert result == (
        VisualizationAnnotation(
            timestamp=20.0,
            label="b",
        ),
    )
