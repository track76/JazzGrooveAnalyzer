from jga.visualization.pipeline.visualization_projection_pipeline import (
    VisualizationProjectionPipeline,
)

from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
)

from jga.visualization.visualization_annotation import (
    VisualizationAnnotation,
)


def test_projection_pipeline_preserves_annotations():

    annotation = VisualizationAnnotation(
        timestamp=10.0,
        label="metric_event",
    )

    scene = ScientificVisualizationScene(
        annotations=(
            annotation,
        ),
    )

    projected = (
        VisualizationProjectionPipeline()
        .project(
            scene,
        )
    )

    assert projected.annotations == (
        annotation,
    )
