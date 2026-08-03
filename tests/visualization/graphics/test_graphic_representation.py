from jga.visualization.graphic_representation import (
    GraphicRepresentation,
)


def test_graphic_representation_exists():

    representation = GraphicRepresentation()

    assert representation is not None
