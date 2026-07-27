from jga.representation.projection import (
    ProjectionInput,
    ScientificProjectionEngine,
)


def test_projection_pipeline_accepts_projection_input():
    engine = ScientificProjectionEngine()

    projection_input = ProjectionInput(
        representation_object=object(),
    )

    assert engine.project(projection_input) is projection_input
