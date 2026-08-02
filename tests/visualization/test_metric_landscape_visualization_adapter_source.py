from jga.visualization.metric_landscape_visualization_adapter import (
    MetricLandscapeVisualizationAdapter,
)

from jga.representation.metric_landscape import (
    MetricLandscape,
)


def test_adapter_accepts_source_landscape():

    landscape = MetricLandscape()

    trajectory = (
        MetricLandscapeVisualizationAdapter()
        .adapt(
            landscape,
        )
    )

    assert trajectory is not None
