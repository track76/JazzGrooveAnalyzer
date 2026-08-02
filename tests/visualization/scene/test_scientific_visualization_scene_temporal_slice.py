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


def descriptor():

    return VisualizationTrajectoryDescriptor(
        identifier="ensemble",
        trajectory=VisualTrajectory(
            points=(
                VisualPoint(
                    x=0.0,
                    y=0.0,
                    time=0.0,
                ),
                VisualPoint(
                    x=1.0,
                    y=1.0,
                    time=10.0,
                ),
                VisualPoint(
                    x=2.0,
                    y=2.0,
                    time=20.0,
                ),
            ),
        ),
    )


def test_scene_temporal_slice():

    scene = ScientificVisualizationScene(
        trajectories=(
            descriptor(),
        ),
    )

    sliced = scene.slice_time(
        start_time=5.0,
        end_time=15.0,
    )

    assert (
        sliced.trajectories[0]
        .trajectory
        .point_count()
        == 1
    )

    assert (
        sliced.trajectories[0]
        .trajectory
        .first_point()
        .time
        == 10.0
    )
