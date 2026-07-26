from jga.representation.builders.metric_landscape_builder import (
    MetricLandscapeBuilder,
)
from jga.representation.metric_landscape import (
    MetricLandscape,
)


def test_metric_landscape_builder_exists():

    assert MetricLandscapeBuilder is not None


def test_metric_landscape_builder_creates_landscape():

    builder = MetricLandscapeBuilder()

    landscape = builder.build()

    assert isinstance(
        landscape,
        MetricLandscape,
    )


def test_metric_landscape_builder_preserves_portraits():

    builder = MetricLandscapeBuilder()

    portraits = ("portrait",)

    landscape = builder.build(
        metric_cluster_portraits=portraits,
    )

    assert (
        landscape.metric_cluster_portraits
        is portraits
    )
