from pathlib import Path

from tests.support.domain_objects import (
    make_metric_cluster,
)

from jga.representation.pipeline import (
    RepresentationPipeline,
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


def test_figure_exporter_creates_png(tmp_path: Path):

    representation = (
        RepresentationPipeline().run(
            metric_clusters=(
                make_metric_cluster(),
            ),
        )
    )

    trajectory = (
        MetricLandscapeVisualizationAdapter().adapt(
            representation.metric_landscape,
        )
    )

    figure = (
        MatplotlibRenderer().render(
            trajectory,
        )
    )

    destination = tmp_path / "metric_plot.png"

    FigureExporter().export(
        figure,
        str(destination),
    )

    assert destination.exists()
    assert destination.stat().st_size > 0
