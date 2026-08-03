from jga.visualization.graphic_composition import (
    GraphicComposition,
)


def test_graphic_composition_default_state():

    composition = GraphicComposition()

    assert composition.elements == ()

    assert composition.metadata == {}

    assert composition.is_valid()
