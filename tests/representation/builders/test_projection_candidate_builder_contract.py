from jga.representation.builders.projection_candidate_builder import (
    ProjectionCandidateBuilder,
)


def test_builder_exposes_build_method():

    builder = ProjectionCandidateBuilder()

    assert callable(builder.build)
