from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
)

from jga.visualization.visualization_trajectory_descriptor import (
    VisualizationTrajectoryDescriptor,
)

from jga.visualization.visual_trajectory import (
    VisualTrajectory,
)


def test_scene_contains_identifier():

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
        ),
    )

    assert scene.contains("bass")
    assert scene.contains("piano")
    assert not scene.contains("drums")
