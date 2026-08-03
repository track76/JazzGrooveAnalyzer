from jga.visualization.point_element import (
    PointElement,
)


def test_point_element_has_point_type():

    element = PointElement()

    assert element.element_type == "point"
