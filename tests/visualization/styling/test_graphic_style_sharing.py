from jga.visualization.graphic_style import (
    GraphicStyle,
)

from jga.visualization.line_element import (
    LineElement,
)

from jga.visualization.point_element import (
    PointElement,
)


def test_graphic_style_can_be_shared():

    style = GraphicStyle()

    line = LineElement(
        style=style,
    )

    point = PointElement(
        style=style,
    )

    assert line.style is style
    assert point.style is style
