from jga.visualization.graphic_composition import (
    GraphicComposition,
)


def test_graphic_composition_exists():

    composition = GraphicComposition()

    assert composition is not None
