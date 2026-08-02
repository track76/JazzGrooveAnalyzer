import pytest

from jga.visualization.visual_point import VisualPoint


def test_creates_visual_point():
    point = VisualPoint(
        x=1.0,
        y=2.0,
        time=3.5,
    )

    assert point.x == 1.0
    assert point.y == 2.0
    assert point.time == 3.5


def test_rejects_negative_time():
    with pytest.raises(ValueError):
        VisualPoint(
            x=0.0,
            y=0.0,
            time=-0.1,
        )


def test_visual_point_is_immutable():
    point = VisualPoint(
        x=1.0,
        y=2.0,
        time=3.0,
    )

    with pytest.raises(Exception):
        point.time = 10.0
