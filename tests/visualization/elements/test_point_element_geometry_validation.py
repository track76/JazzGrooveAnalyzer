from jga.visualization.point_element import (
    PointElement,
)


def test_point_element_with_position_is_valid():

    element = PointElement(
        position=(
            0.5,
            0.5,
        ),
    )

    assert element.is_valid()
