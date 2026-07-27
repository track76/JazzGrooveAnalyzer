from jga.representation.builders.projection_candidate_builder import (
    ProjectionCandidateBuilder,
)


def test_builder_returns_projection_candidate():

    builder = ProjectionCandidateBuilder()

    obj = object()

    candidate = builder.build(obj)

    assert candidate.representation_object is obj
