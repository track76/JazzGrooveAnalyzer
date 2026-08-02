from jga.representation.metric_landscape import (
    MetricLandscape,
)

from jga.visualization.scientific_visualization_frame import (
    ScientificVisualizationFrame,
)


def test_visualization_frame_preserves_landscape():

    landscape = MetricLandscape()

    frame = ScientificVisualizationFrame(
        metric_landscape=landscape,
    )

    assert (
        frame.metric_landscape
        is landscape
    )


def test_visualization_frame_is_immutable():

    frame = ScientificVisualizationFrame(
        metric_landscape=MetricLandscape(),
    )

    try:
        frame.metric_landscape = MetricLandscape()
        assert False
    except Exception:
        assert True
