from jga.representation.metric_landscape import (
    MetricLandscape,
)

from jga.representation.representation_result import (
    RepresentationResult,
)


def test_representation_result_creates_default_ensemble_landscape():

    landscape = MetricLandscape()

    result = RepresentationResult(
        metric_landscape=landscape,
    )

    assert result.metric_landscapes == {
        "ensemble": landscape,
    }

    assert (
        result.metric_landscapes["ensemble"]
        is result.metric_landscape
    )
