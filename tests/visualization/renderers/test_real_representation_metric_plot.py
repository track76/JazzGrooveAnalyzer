from tests.support.domain_objects import (
    make_metric_cluster,
)

from jga.representation.pipeline import (
    RepresentationPipeline,
)

from jga.visualization.metric_landscape_visualization_adapter import (
    MetricLandscapeVisualizationAdapter,
)

from jga.visualization.renderers.matplotlib_renderer import (
    MatplotlibRenderer,
)


def test_real_representation_result_produces_metric_plot():

    representation_result = (
        RepresentationPipeline()
        .run(
            metric_clusters=(
                make_metric_cluster(),
            ),
        )
    )

    landscape = (
        representation_result
        .metric_landscape
    )

    trajectory = (
        MetricLandscapeVisualizationAdapter()
        .adapt(
            landscape
        )
    )

    figure = (
        MatplotlibRenderer()
        .render(
            trajectory
        )
    )

    assert figure is not None

    assert len(
        figure.axes
    ) == 1
