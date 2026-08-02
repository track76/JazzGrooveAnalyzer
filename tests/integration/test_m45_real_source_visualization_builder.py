from jga.pipeline.default_analysis_pipeline import (
    AnalysisPipeline,
)

from jga.visualization.source_visualization_builder import (
    SourceVisualizationBuilder,
)

from jga.visualization.renderers.matplotlib_renderer import (
    MatplotlibRenderer,
)


def test_m45_real_source_visualization_builder():

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

    assert scene.contains(
        "ensemble"
    )

    assert (
        scene.total_points()
        > 0
    )

    figure = (
        MatplotlibRenderer()
        .render_scene(
            scene,
        )
    )

    assert figure is not None
