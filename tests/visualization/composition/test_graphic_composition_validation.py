from jga.visualization.graphic_composition import (
    GraphicComposition,
)


def test_graphic_composition_is_valid():

    composition = GraphicComposition()

    assert composition.is_valid()
