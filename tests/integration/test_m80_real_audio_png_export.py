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

from jga.visualization.exporters.figure_exporter import (
    FigureExporter,
)


def test_m80_real_audio_png_export():

    context = AnalysisPipeline().analyze(
        "recordings/III_Chet Baker - I fall in love too easily.mp3"
    )

    trajectory = (
        MetricLandscapeVisualizationAdapter().adapt(
            context.representation_result.metric_landscape
        )
    )

    figure = MatplotlibRenderer().render(
        trajectory
    )

    output = Path(
        "output/jga_metric_landscape_real_audio.png"
    )

    FigureExporter().export(
        figure,
        str(output),
    )

    assert output.exists()
    assert output.stat().st_size > 0

    print()
    print("PNG generated:")
    print(output.resolve())
