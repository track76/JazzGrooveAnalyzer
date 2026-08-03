from jga.visualization.point_element import (
    PointElement,
)


def test_point_element_exposes_position():

    element = PointElement(
        position=(
            0.5,
            0.5,
        ),
    )

    assert element.position == (
        0.5,
        0.5,
    )
