from jga.visualization.graphic_composition import (
    GraphicComposition,
)


def test_graphic_composition_exposes_metadata():

    composition = GraphicComposition(
        metadata={
            "purpose": "scientific_scene",
        },
    )

    assert composition.metadata == {
        "purpose": "scientific_scene",
    }
