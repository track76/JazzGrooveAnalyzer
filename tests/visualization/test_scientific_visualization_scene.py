from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
)

from jga.visualization.visual_trajectory import (
    VisualTrajectory,
)

from jga.visualization.visualization_trajectory_descriptor import (
    VisualizationTrajectoryDescriptor,
)


def test_scene_accepts_identified_trajectories():

    descriptor_a = VisualizationTrajectoryDescriptor(
        identifier="bass",
        trajectory=VisualTrajectory(),
    )

    descriptor_b = VisualizationTrajectoryDescriptor(
        identifier="drums",
        trajectory=VisualTrajectory(),
    )

    scene = ScientificVisualizationScene(
        trajectories=(
            descriptor_a,
            descriptor_b,
        )
    )

    assert scene.trajectories == (
        descriptor_a,
        descriptor_b,
    )


def test_scene_preserves_descriptor_identity():

    descriptor = VisualizationTrajectoryDescriptor(
        identifier="piano",
        trajectory=VisualTrajectory(),
    )

    scene = ScientificVisualizationScene(
        trajectories=(
            descriptor,
        )
    )

    assert scene.trajectories[0] is descriptor
