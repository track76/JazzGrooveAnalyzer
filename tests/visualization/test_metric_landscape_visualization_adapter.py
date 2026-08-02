from jga.representation.metric_landscape import (
    MetricLandscape,
)

from jga.representation.metric_trajectory import (
    MetricTrajectory,
)

from jga.representation.scientific_coordinate import (
    ScientificCoordinate,
)

from jga.representation.standard_axes import (
    METRIC_TEMPORAL_DISPLACEMENT_AXIS,
)

from jga.representation.metric_point import (
    MetricPoint,
)

from jga.visualization.metric_landscape_visualization_adapter import (
    MetricLandscapeVisualizationAdapter,
)


def test_adapter_projects_metric_coordinates():

    point = MetricPoint(
        event=None,
        coordinate=ScientificCoordinate(
            value=12.5,
            axis=METRIC_TEMPORAL_DISPLACEMENT_AXIS,
        ),
    )

    landscape = MetricLandscape(
        metric_trajectory=MetricTrajectory(
            metric_points=(
                point,
            )
        )
    )

    trajectory = (
        MetricLandscapeVisualizationAdapter()
        .adapt(landscape)
    )

    assert trajectory.points[0].x == 0.0
    assert trajectory.points[0].y == 12.5
