from jga.representation.metric_landscape import (
    MetricLandscape,
)
from jga.representation.metric_trajectory import (
    MetricTrajectory,
)


def test_metric_landscape_stores_metric_trajectory():

    trajectory = MetricTrajectory()

    landscape = MetricLandscape(
        metric_trajectory=trajectory,
    )

    assert landscape.metric_trajectory is trajectory
