from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
)

from jga.visualization.visualization_annotation import (
    VisualizationAnnotation,
)


def test_scene_queries_annotations_by_label():

    scene = ScientificVisualizationScene(
        annotations=(
            VisualizationAnnotation(
                timestamp=10.0,
                label="metric_event",
            ),
            VisualizationAnnotation(
                timestamp=20.0,
                label="beat_reference",
            ),
        ),
    )

    result = scene.find_annotations(
        "metric_event",
    )

    assert result == (
        VisualizationAnnotation(
            timestamp=10.0,
            label="metric_event",
        ),
    )
