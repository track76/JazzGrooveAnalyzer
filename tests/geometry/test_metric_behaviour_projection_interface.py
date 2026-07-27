from inspect import isabstract

from jga.interfaces.geometry import (
    MetricBehaviourProjection,
)


def test_projection_is_abstract():

    assert isabstract(
        MetricBehaviourProjection
    )


def test_projection_has_project():

    assert hasattr(
        MetricBehaviourProjection,
        "project",
    )
