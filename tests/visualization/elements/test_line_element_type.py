from jga.visualization.line_element import (
    LineElement,
)


def test_line_element_has_line_type():

    element = LineElement()

    assert element.element_type == "line"
