from jga.representation.metric_landscape import (
    MetricLandscape,
)

from jga.representation.representation_result import (
    RepresentationResult,
)

from jga.visualization.comparative_visualization_builder import (
    ComparativeVisualizationBuilder,
)


def test_comparative_visualization_builder():

    bass = MetricLandscape()

    piano = MetricLandscape()

    result = RepresentationResult(
        metric_landscape=bass,
        metric_landscapes={
            "bass": bass,
            "piano": piano,
        },
    )

    scene = (
        ComparativeVisualizationBuilder()
        .build(
            result,
            sources=(
                "bass",
                "piano",
            ),
        )
    )

    assert scene.contains(
        "bass"
    )

    assert scene.contains(
        "piano"
    )
