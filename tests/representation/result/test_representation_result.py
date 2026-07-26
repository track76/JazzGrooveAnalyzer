from jga.representation.representation_result import (
    RepresentationResult,
)


def test_representation_result_exists():

    assert RepresentationResult is not None


def test_representation_result_defaults_to_empty():

    result = RepresentationResult()

    assert result.metric_landscape is None
