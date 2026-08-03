from jga.visualization.graphic_style import (
    GraphicStyle,
)


def test_graphic_style_exposes_metadata():

    style = GraphicStyle(
        metadata={
            "purpose": "scientific_default",
        },
    )

    assert style.metadata == {
        "purpose": "scientific_default",
    }
