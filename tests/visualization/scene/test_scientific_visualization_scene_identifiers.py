from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
)

from jga.visualization.visualization_trajectory_descriptor import (
    VisualizationTrajectoryDescriptor,
)

from jga.visualization.visual_trajectory import (
    VisualTrajectory,
)


def test_scene_returns_available_identifiers():

    scene = ScientificVisualizationScene(
        trajectories=(
            VisualizationTrajectoryDescriptor(
                identifier="bass",
                trajectory=VisualTrajectory(),
            ),
            VisualizationTrajectoryDescriptor(
                identifier="piano",
                trajectory=VisualTrajectory(),
            ),
            VisualizationTrajectoryDescriptor(
                identifier="drums",
                trajectory=VisualTrajectory(),
            ),
        ),
    )

    assert scene.identifiers() == (
        "bass",
        "piano",
        "drums",
    )
