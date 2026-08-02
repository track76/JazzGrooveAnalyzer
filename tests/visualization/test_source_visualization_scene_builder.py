from jga.representation.metric_landscape import (
    MetricLandscape,
)

from jga.representation.representation_result import (
    RepresentationResult,
)

from jga.visualization.metric_landscape_visualization_adapter import (
    MetricLandscapeVisualizationAdapter,
)

from jga.visualization.visual_trajectory_scene_adapter import (
    VisualTrajectorySceneAdapter,
)


def test_source_landscape_can_become_scene():

    bass = MetricLandscape()

    result = RepresentationResult(
        metric_landscape=bass,
        metric_landscapes={
            "bass": bass,
        },
    )

    trajectory = (
        MetricLandscapeVisualizationAdapter()
        .adapt_source(
            result,
            source="bass",
        )
    )

    scene = (
        VisualTrajectorySceneAdapter()
        .adapt(
            trajectory,
            identifier="bass",
        )
    )

    assert scene.contains(
        "bass"
    )
