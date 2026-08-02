from uuid import uuid4

from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
)

from jga.visualization.visualization_annotation import (
    VisualizationAnnotation,
)


def test_scene_queries_annotation_by_reference():

    reference = uuid4()

    scene = ScientificVisualizationScene(
        annotations=(
            VisualizationAnnotation(
                timestamp=10.0,
                label="metric_event",
                reference_id=reference,
            ),
        ),
    )

    result = scene.annotation_for_reference(
        reference,
    )

    assert result == VisualizationAnnotation(
        timestamp=10.0,
        label="metric_event",
        reference_id=reference,
    )
