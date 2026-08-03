from jga.visualization.line_element import (
    LineElement,
)


def test_line_element_exposes_points():

    element = LineElement(
        points=(
            (0.0, 0.0),
            (1.0, 1.0),
        ),
    )

    assert element.points == (
        (0.0, 0.0),
        (1.0, 1.0),
    )
