from jga.visualization.graphic_scene import (
    GraphicScene,
)

from jga.visualization.graphic_style import (
    GraphicStyle,
)


def test_graphic_scene_accepts_style():

    style = GraphicStyle()

    scene = GraphicScene(
        style=style,
    )

    assert scene.style is style
