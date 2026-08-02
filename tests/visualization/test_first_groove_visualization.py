from jga.domain.elementary_metric_event import (
    ElementaryMetricEvent,
)

from jga.representation.metric_point import (
    MetricPoint,
)

from jga.representation.metric_trajectory import (
    MetricTrajectory,
)

from jga.representation.metric_landscape import (
    MetricLandscape,
)

from jga.representation.scientific_coordinate import (
    ScientificCoordinate,
)

from jga.representation.standard_axes import (
    METRIC_TEMPORAL_DISPLACEMENT_AXIS,
)

from jga.visualization.metric_landscape_visualization_adapter import (
    MetricLandscapeVisualizationAdapter,
)

from jga.visualization.ascii_renderer import (
    ASCIIRenderer,
)


def test_first_groove_visualization_pipeline():

    points = (
        MetricPoint(
            event=ElementaryMetricEvent(
                id=None,
                contributor_id=None,
                timestamp=0.0,
                confidence=1.0,
                created_at=None,
            ),
            coordinate=ScientificCoordinate(
                value=-5.0,
                axis=METRIC_TEMPORAL_DISPLACEMENT_AXIS,
            ),
        ),
        MetricPoint(
            event=ElementaryMetricEvent(
                id=None,
                contributor_id=None,
                timestamp=1.0,
                confidence=1.0,
                created_at=None,
            ),
            coordinate=ScientificCoordinate(
                value=10.0,
                axis=METRIC_TEMPORAL_DISPLACEMENT_AXIS,
            ),
        ),
    )

    landscape = MetricLandscape(
        metric_trajectory=MetricTrajectory(
            metric_points=points,
        )
    )

    trajectory = (
        MetricLandscapeVisualizationAdapter()
        .adapt(landscape)
    )

    output = (
        ASCIIRenderer()
        .render(trajectory)
    )

    assert output == (
        "(0.0,-5.0)\n"
        "(1.0,10.0)"
    )
