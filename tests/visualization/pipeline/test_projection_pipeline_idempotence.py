from jga.visualization.pipeline.visualization_projection_pipeline import (
    VisualizationProjectionPipeline,
)

from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
)


def test_empty_pipeline_returns_same_scene():

    scene = ScientificVisualizationScene()

    pipeline = VisualizationProjectionPipeline()

    projected = pipeline.project(
        scene,
    )

    assert projected is scene
