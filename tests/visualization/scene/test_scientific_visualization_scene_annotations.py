from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
)

from jga.visualization.visualization_annotation import (
    VisualizationAnnotation,
)


def test_scene_supports_annotations():

    annotation = VisualizationAnnotation(
        timestamp=10.0,
        label="metric_event",
    )

    scene = ScientificVisualizationScene(
        annotations=(
            annotation,
        ),
    )

    assert scene.annotations == (
        annotation,
    )
