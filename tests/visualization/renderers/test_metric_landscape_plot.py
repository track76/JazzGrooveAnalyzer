import matplotlib.figure

from jga.representation.metric_landscape import (
    MetricLandscape,
)
from jga.representation.metric_point import (
    MetricPoint,
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
from jga.visualization.metric_landscape_visualization_adapter import (
    MetricLandscapeVisualizationAdapter,
)
from jga.visualization.renderers.matplotlib_renderer import (
    MatplotlibRenderer,
)

from tests.factories.elementary_metric_event_factory import (
    make_elementary_metric_event,
)


def test_metric_landscape_produces_scientific_plot():

    metric_points = (
        MetricPoint(
            event=make_elementary_metric_event(
                timestamp=0.0,
            ),
            coordinate=ScientificCoordinate(
                value=-8.0,
                axis=METRIC_TEMPORAL_DISPLACEMENT_AXIS,
            ),
        ),
        MetricPoint(
            event=make_elementary_metric_event(
                timestamp=1.0,
            ),
            coordinate=ScientificCoordinate(
                value=4.0,
                axis=METRIC_TEMPORAL_DISPLACEMENT_AXIS,
            ),
        ),
        MetricPoint(
            event=make_elementary_metric_event(
                timestamp=2.0,
            ),
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

    renderer = MatplotlibRenderer()

    figure = renderer.render(
        trajectory,
    )

    assert isinstance(
        figure,
        matplotlib.figure.Figure,
    )
