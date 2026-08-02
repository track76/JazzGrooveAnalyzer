from jga.visualization.visual_trajectory import (
    VisualTrajectory,
)

from jga.visualization.visualization_trajectory_descriptor import (
    VisualizationTrajectoryDescriptor,
)


def test_descriptor_preserves_identifier():

    trajectory = VisualTrajectory()

    descriptor = VisualizationTrajectoryDescriptor(
        identifier="bass",
        trajectory=trajectory,
    )

    assert descriptor.identifier == "bass"


def test_descriptor_preserves_trajectory_identity():

    trajectory = VisualTrajectory()

    descriptor = VisualizationTrajectoryDescriptor(
        identifier="drums",
        trajectory=trajectory,
    )

    assert descriptor.trajectory is trajectory
