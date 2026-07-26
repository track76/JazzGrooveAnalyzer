from jga.representation.metric_landscape import (
    MetricLandscape,
)
from jga.representation.representation_result import (
    RepresentationResult,
)


def test_representation_result_stores_metric_landscape():

    landscape = MetricLandscape()

    result = RepresentationResult(
        metric_landscape=landscape,
    )

    assert result.metric_landscape is landscape
