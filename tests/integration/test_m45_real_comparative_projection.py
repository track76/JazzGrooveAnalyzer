from jga.pipeline.default_analysis_pipeline import (
    AnalysisPipeline,
)

from jga.visualization.comparative_visualization_builder import (
    ComparativeVisualizationBuilder,
)

from jga.visualization.pipeline.visualization_projection_pipeline import (
    VisualizationProjectionPipeline,
)

from jga.visualization.renderers.matplotlib_renderer import (
    MatplotlibRenderer,
)


def test_m45_real_comparative_projection():

    context = (
        AnalysisPipeline()
        .analyze(
            "recordings/III_Chet Baker - I fall in love too easily.mp3"
        )
    )

    scene = (
        ComparativeVisualizationBuilder()
        .build(
            context.representation_result,
            sources=(
                "ensemble",
            ),
        )
    )

    projected = (
        VisualizationProjectionPipeline()
        .project(
            scene,
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
