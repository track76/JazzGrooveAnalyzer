from jga.visualization.comparative_visualization_builder import (
    ComparativeVisualizationBuilder,
)

from jga.visualization.temporal_visualization_window import (
    TemporalVisualizationWindow,
)

from jga.representation.metric_landscape import (
    MetricLandscape,
)

from jga.representation.representation_result import (
    RepresentationResult,
)


def test_comparative_scene_accepts_temporal_window():

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

    window = TemporalVisualizationWindow(
        start_time=10.0,
        end_time=20.0,
    )

    sliced = scene.slice(
        window,
    )

    assert sliced.contains(
        "bass"
    )

    assert sliced.contains(
        "piano"
    )
