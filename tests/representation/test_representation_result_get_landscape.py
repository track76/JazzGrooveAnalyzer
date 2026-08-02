import pytest

from jga.representation.metric_landscape import (
    MetricLandscape,
)

from jga.representation.representation_result import (
    RepresentationResult,
)


def test_representation_result_get_landscape():

    bass = MetricLandscape()

    result = RepresentationResult(
        metric_landscape=bass,
        metric_landscapes={
            "bass": bass,
        },
    )

    assert (
        result.get_landscape("bass")
        is bass
    )


def test_representation_result_get_unknown_landscape():

    result = RepresentationResult(
        metric_landscape=MetricLandscape(),
    )

    with pytest.raises(
        KeyError,
    ):
        result.get_landscape(
            "piano",
        )
