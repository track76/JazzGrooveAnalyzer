from jga.visualization.visual_point import (
    VisualPoint,
)


def test_visual_point_creation():

    point = VisualPoint(
        x=10.0,
        y=20.0,
    )

    assert point.x == 10.0
    assert point.y == 20.0


def test_visual_point_is_immutable():

    point = VisualPoint(
        x=0.0,
        y=0.0,
    )

    try:
        point.x = 1.0
        assert False
    except Exception:
        assert True
