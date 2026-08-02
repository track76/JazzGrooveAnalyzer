from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
)

from jga.visualization.visualization_annotation import (
    VisualizationAnnotation,
)

from jga.visualization.visualization_output_builder import (
    VisualizationOutputBuilder,
)


def test_visualization_output_contains_annotation_count_metadata():

    scene = ScientificVisualizationScene(
        annotations=(
            VisualizationAnnotation(
                timestamp=10.0,
                label="metric_event",
            ),
            VisualizationAnnotation(
                timestamp=20.0,
                label="metric_event",
            ),
        ),
    )

    output = (
        VisualizationOutputBuilder()
        .build(scene)
    )

    assert (
        output.metadata["annotation_count"]
        == 2
    )
