from jga.representation.builders.metric_landscape_builder import (
    MetricLandscapeBuilder,
)
from jga.representation.metric_trajectory import (
    MetricTrajectory,
)


def test_metric_landscape_builder_accepts_metric_trajectory():

    builder = MetricLandscapeBuilder()

    trajectory = MetricTrajectory()

    landscape = builder.build(
        metric_cluster_portraits=(),
        metric_trajectory=trajectory,
    )

    assert landscape.metric_trajectory is trajectory
