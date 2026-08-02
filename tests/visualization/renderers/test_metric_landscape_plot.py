from jga.representation.metric_landscape import (
    MetricLandscape,
)

from jga.representation.metric_trajectory import (
    MetricTrajectory,
)

from jga.representation.metric_point import (
    MetricPoint,
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

from jga.visualization.renderers.matplotlib_renderer import (
    MatplotlibRenderer,
)


def test_metric_landscape_produces_scientific_plot():

    metric_points = (
        MetricPoint(
            event=None,
            coordinate=ScientificCoordinate(
                value=-8.0,
                axis=METRIC_TEMPORAL_DISPLACEMENT_AXIS,
            ),
        ),
        MetricPoint(
            event=None,
            coordinate=ScientificCoordinate(
                value=4.0,
                axis=METRIC_TEMPORAL_DISPLACEMENT_AXIS,
            ),
        ),
        MetricPoint(
            event=None,
            coordinate=ScientificCoordinate(
                value=12.0,
                axis=METRIC_TEMPORAL_DISPLACEMENT_AXIS,
            ),
        ),
    )

    landscape = MetricLandscape(
        metric_trajectory=MetricTrajectory(
            metric_points=metric_points,
        )
    )

    trajectory = (
        MetricLandscapeVisualizationAdapter()
        .adapt(landscape)
    )

    figure = (
        MatplotlibRenderer()
        .render(trajectory)
    )

    assert figure is not None
    assert len(
        figure.axes
    ) == 1
