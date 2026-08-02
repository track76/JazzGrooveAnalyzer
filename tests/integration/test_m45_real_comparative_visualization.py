from jga.pipeline.default_analysis_pipeline import (
    AnalysisPipeline,
)

from jga.visualization.comparative_visualization_builder import (
    ComparativeVisualizationBuilder,
)

from jga.visualization.renderers.matplotlib_renderer import (
    MatplotlibRenderer,
)


def test_m45_real_comparative_visualization():

    context = (
        AnalysisPipeline()
        .analyze(
            "recordings/III_Chet Baker - I fall in love too easily.mp3"
        )
    )

    result = (
        context
        .representation_result
    )

    scene = (
        ComparativeVisualizationBuilder()
        .build(
            result,
            sources=(
                "ensemble",
            ),
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
