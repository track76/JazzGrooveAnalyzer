from jga.visualization.line_element import (
    LineElement,
)


def test_line_element_with_points_is_valid():

    element = LineElement(
        points=(
            (0.0, 0.0),
            (1.0, 1.0),
        ),
    )

    assert element.is_valid()
