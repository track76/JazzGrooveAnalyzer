from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
)

from jga.visualization.visualization_trajectory_descriptor import (
    VisualizationTrajectoryDescriptor,
)

from jga.visualization.visual_trajectory import (
    VisualTrajectory,
)

from jga.visualization.visual_point import (
    VisualPoint,
)


def descriptor(identifier):

    return VisualizationTrajectoryDescriptor(
        identifier=identifier,
        trajectory=VisualTrajectory(
            points=(
                VisualPoint(
                    x=0.0,
                    y=0.0,
                    time=10.0,
                ),
                VisualPoint(
                    x=1.0,
                    y=1.0,
                    time=20.0,
                ),
            ),
        ),
    )


def test_scene_temporal_slice_preserves_sources():

    scene = ScientificVisualizationScene(
        trajectories=(
            descriptor("bass"),
            descriptor("piano"),
        ),
    )

    sliced = scene.slice_time(
        start_time=15.0,
        end_time=25.0,
    )

    assert sliced.contains("bass")

    assert sliced.contains("piano")

    assert (
        sliced.total_points()
        == 2
    )
