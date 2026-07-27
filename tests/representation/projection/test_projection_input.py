from dataclasses import is_dataclass

from jga.representation.projection.projection_input import ProjectionInput


def test_projection_input_is_dataclass():
    assert is_dataclass(ProjectionInput)


def test_projection_input_is_frozen():
    assert ProjectionInput.__dataclass_params__.frozen


def test_projection_input_preserves_representation_object():
    obj = object()

    projection_input = ProjectionInput(
        representation_object=obj,
    )

    assert projection_input.representation_object is obj
