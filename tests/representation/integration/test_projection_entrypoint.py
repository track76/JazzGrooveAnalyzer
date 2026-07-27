from jga.representation.projection import (
    ProjectionInput,
    ScientificProjectionEngine,
)


def test_representation_entrypoint_exists():

    engine = ScientificProjectionEngine()

    projection = ProjectionInput(
        representation_object=object(),
    )

    result = engine.project(projection)

    assert result is projection
