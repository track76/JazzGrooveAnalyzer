from jga.pipeline.default_analysis_pipeline import (
    AnalysisPipeline,
)

from jga.visualization.metric_landscape_visualization_adapter import (
    MetricLandscapeVisualizationAdapter,
)

from jga.visualization.visual_trajectory_scene_adapter import (
    VisualTrajectorySceneAdapter,
)

from jga.visualization.renderers.matplotlib_renderer import (
    MatplotlibRenderer,
)


def test_m45_multi_trajectory_visualization():

    context = (
        AnalysisPipeline()
        .analyze(
            "recordings/III_Chet Baker - I fall in love too easily.mp3"
        )
    )

    landscape = (
        context
        .representation_result
        .metric_landscape
    )

    trajectory = (
        MetricLandscapeVisualizationAdapter()
        .adapt(
            landscape
        )
    )

    scene = (
        VisualTrajectorySceneAdapter()
        .adapt(
            trajectory,
            identifier="ensemble",
        )
    )

    renderer = (
        MatplotlibRenderer()
    )

    figure = renderer.render_scene(
        scene,
    )

    assert figure is not None

    assert (
        scene.trajectory_count()
        >= 1
    )

    assert (
        scene.total_points()
        > 0
    )
