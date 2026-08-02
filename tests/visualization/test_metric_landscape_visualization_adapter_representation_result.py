from jga.visualization.metric_landscape_visualization_adapter import (
    MetricLandscapeVisualizationAdapter,
)

from jga.representation.metric_landscape import (
    MetricLandscape,
)

from jga.representation.representation_result import (
    RepresentationResult,
)


def test_adapter_extracts_selected_source_landscape():

    bass = MetricLandscape()

    result = RepresentationResult(
        metric_landscape=bass,
        metric_landscapes={
            "bass": bass,
        },
    )

    trajectory = (
        MetricLandscapeVisualizationAdapter()
        .adapt_source(
            result,
            source="bass",
        )
    )

    assert trajectory is not None
