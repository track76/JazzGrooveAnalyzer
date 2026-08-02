from jga.pipeline.default_analysis_pipeline import (
    AnalysisPipeline,
)

from jga.visualization.metric_landscape_visualization_adapter import (
    MetricLandscapeVisualizationAdapter,
)

from jga.visualization.pipeline.visualization_projection_pipeline import (
    VisualizationProjectionPipeline,
)

from jga.visualization.projectors.temporal_projector_adapter import (
    TemporalProjectorAdapter,
)

from jga.visualization.projectors.viewport_projector_adapter import (
    ViewportProjectorAdapter,
)

from jga.visualization.temporal_visualization_window import (
    TemporalVisualizationWindow,
)

from jga.visualization.scientific_visualization_viewport import (
    ScientificVisualizationViewport,
)

from jga.visualization.visual_trajectory_scene_adapter import (
    VisualTrajectorySceneAdapter,
)

from jga.visualization.renderers.matplotlib_renderer import (
    MatplotlibRenderer,
)


def test_m43_real_visualization_exploration():

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

    pipeline = (
        VisualizationProjectionPipeline(
            projectors=(
                TemporalProjectorAdapter(
                    TemporalVisualizationWindow(
                        start_time=80.0,
                        end_time=120.0,
                    ),
                ),
                ViewportProjectorAdapter(
                    ScientificVisualizationViewport(
                        x_min=0.0,
                        x_max=500.0,
                        y_min=-100.0,
                        y_max=100.0,
                    ),
                ),
            ),
        )
    )

    projected = pipeline.project(
        scene,
    )

    figure = (
        MatplotlibRenderer()
        .render(
            projected.trajectories[0].trajectory
        )
    )

    assert figure is not None

    assert (
        len(
            projected.trajectories[0]
            .trajectory.points
        )
        > 0
    )
