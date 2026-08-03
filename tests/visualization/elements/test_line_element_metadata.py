from jga.visualization.line_element import (
    LineElement,
)


def test_line_element_exposes_metadata():

    element = LineElement(
        metadata={
            "role": "trajectory",
        },
    )

    assert element.metadata == {
        "role": "trajectory",
    }
