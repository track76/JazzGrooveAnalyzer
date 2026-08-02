from jga.visualization.pipeline.visualization_projection_pipeline import (
    VisualizationProjectionPipeline,
)

from jga.visualization.temporal_visualization_window import (
    TemporalVisualizationWindow,
)

from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
)


def test_projection_pipeline_accepts_temporal_window():

    pipeline = VisualizationProjectionPipeline()

    scene = ScientificVisualizationScene()

    window = TemporalVisualizationWindow(
        start_time=10.0,
        end_time=20.0,
    )

    projected = pipeline.project(
        scene,
        window,
    )

    assert projected is not None
