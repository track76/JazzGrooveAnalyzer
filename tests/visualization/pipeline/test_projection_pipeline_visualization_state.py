from jga.visualization.pipeline.visualization_projection_pipeline import (
    VisualizationProjectionPipeline,
)

from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
)

from jga.visualization.visualization_state import (
    VisualizationState,
)


def test_projection_pipeline_accepts_visualization_state():

    pipeline = VisualizationProjectionPipeline()

    scene = ScientificVisualizationScene()

    state = VisualizationState()

    projected = pipeline.project(
        scene,
        state,
    )

    assert projected is not None
