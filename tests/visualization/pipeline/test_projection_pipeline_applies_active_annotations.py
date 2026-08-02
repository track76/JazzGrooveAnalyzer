from jga.visualization.pipeline.visualization_projection_pipeline import (
    VisualizationProjectionPipeline,
)

from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
)

from jga.visualization.visualization_annotation import (
    VisualizationAnnotation,
)

from jga.visualization.visualization_state import (
    VisualizationState,
)


def test_projection_pipeline_applies_active_annotations():

    annotation = VisualizationAnnotation(
        timestamp=10.0,
        label="metric_event",
    )

    scene = ScientificVisualizationScene()

    state = VisualizationState(
        active_annotations=(
            annotation,
        ),
    )

    projected = (
        VisualizationProjectionPipeline()
        .project(
            scene,
            state=state,
        )
    )

    assert projected.annotations == (
        annotation,
    )
