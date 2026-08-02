from jga.pipeline.default_analysis_pipeline import (
    AnalysisPipeline,
)

from jga.visualization.source_visualization_builder import (
    SourceVisualizationBuilder,
)

from jga.visualization.temporal_visualization_window import (
    TemporalVisualizationWindow,
)

from jga.visualization.pipeline.visualization_projection_pipeline import (
    VisualizationProjectionPipeline,
)

from jga.visualization.renderers.matplotlib_renderer import (
    MatplotlibRenderer,
)


def test_m46_real_temporal_window_pipeline():

    context = (
        AnalysisPipeline()
        .analyze(
            "recordings/III_Chet Baker - I fall in love too easily.mp3"
        )
    )

    scene = (
        SourceVisualizationBuilder()
        .build(
            context.representation_result,
            source="ensemble",
        )
    )

    window = TemporalVisualizationWindow(
        start_time=80.0,
        end_time=100.0,
    )

    projected = (
        VisualizationProjectionPipeline()
        .project(
            scene,
            window,
        )
    )

    assert projected.contains(
        "ensemble"
    )

    assert (
        projected.total_points()
        > 0
    )

    figure = (
        MatplotlibRenderer()
        .render_scene(
            projected,
        )
    )

    assert figure is not None
