from pathlib import Path

from jga.pipeline.default_analysis_pipeline import (
    AnalysisPipeline,
)

from jga.visualization.metric_landscape_visualization_adapter import (
    MetricLandscapeVisualizationAdapter,
)

from jga.visualization.renderers.matplotlib_renderer import (
    MatplotlibRenderer,
)


def test_real_audio_produces_scientific_visualization():

    context = (
        AnalysisPipeline()
        .analyze(
            "recordings/III_Chet Baker - I fall in love too easily.mp3"
        )
    )

    assert context.representation_result is not None

    landscape = (
        context
        .representation_result
        .metric_landscape
    )

    assert landscape is not None

    trajectory = (
        MetricLandscapeVisualizationAdapter()
        .adapt(
            landscape
        )
    )

    figure = (
        MatplotlibRenderer()
        .render(
            trajectory
        )
    )

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    figure.savefig(
        output_dir / "chet_baker_metric_plot.png",
        dpi=300,
        bbox_inches="tight",
    )

    assert figure is not None
