from dataclasses import is_dataclass

from jga.representation.candidates import ProjectionCandidate


def test_projection_candidate_is_dataclass():
    assert is_dataclass(ProjectionCandidate)


def test_projection_candidate_is_frozen():
    assert ProjectionCandidate.__dataclass_params__.frozen


def test_projection_candidate_preserves_representation():

    obj = object()

    candidate = ProjectionCandidate(
        representation_object=obj,
    )

    assert candidate.representation_object is obj
