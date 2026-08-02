from jga.representation.representation_result import (
    RepresentationResult,
)

from jga.representation.metric_landscape import (
    MetricLandscape,
)


def test_representation_result_supports_multiple_landscapes():

    bass = MetricLandscape()

    piano = MetricLandscape()

    result = RepresentationResult(
        metric_landscape=bass,
        metric_landscapes={
            "bass": bass,
            "piano": piano,
        },
    )

    assert result.metric_landscapes["bass"] is bass

    assert result.metric_landscapes["piano"] is piano
