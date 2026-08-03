from jga.visualization.point_element import (
    PointElement,
)


def test_point_element_exposes_metadata():

    element = PointElement(
        metadata={
            "role": "marker",
        },
    )

    assert element.metadata == {
        "role": "marker",
    }
