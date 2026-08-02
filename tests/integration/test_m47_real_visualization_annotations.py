from jga.pipeline.default_analysis_pipeline import (
    AnalysisPipeline,
)

from jga.visualization.source_visualization_builder import (
    SourceVisualizationBuilder,
)

from jga.visualization.visualization_annotation import (
    VisualizationAnnotation,
)

from jga.visualization.pipeline.visualization_projection_pipeline import (
    VisualizationProjectionPipeline,
)

from jga.visualization.temporal_visualization_window import (
    TemporalVisualizationWindow,
)

from jga.visualization.renderers.matplotlib_renderer import (
    MatplotlibRenderer,
)


def test_m47_real_visualization_annotations():

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

    annotation = VisualizationAnnotation(
        timestamp=80.0,
        label="metric_event",
    )

    scene = scene.__class__(
        trajectories=scene.trajectories,
        annotations=(
            annotation,
        ),
    )

    window = TemporalVisualizationWindow(
        start_time=75.0,
        end_time=90.0,
    )

    projected = (
        VisualizationProjectionPipeline()
        .project(
            scene,
            window,
        )
    )

    assert projected.annotations == (
        annotation,
    )

    figure = (
        MatplotlibRenderer()
        .render_scene(
            projected,
        )
    )

    assert figure is not None
