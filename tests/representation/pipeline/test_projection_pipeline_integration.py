from jga.representation.candidates import ProjectionCandidate
from jga.representation.projection import ScientificProjectionEngine


def test_projection_pipeline_accepts_candidate():

    engine = ScientificProjectionEngine()

    candidate = ProjectionCandidate(
        representation_object=object(),
    )

    result = engine.project(candidate)

    assert result is candidate
