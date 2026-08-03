from jga.visualization.line_element import (
    LineElement,
)


def test_line_element_is_valid():

    element = LineElement()

    assert element.is_valid()
