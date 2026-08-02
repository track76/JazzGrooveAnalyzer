from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
)

from jga.visualization.visualization_trajectory_descriptor import (
    VisualizationTrajectoryDescriptor,
)

from jga.visualization.visual_trajectory import (
    VisualTrajectory,
)


def test_scene_returns_selected_trajectory():

    bass = VisualizationTrajectoryDescriptor(
        identifier="bass",
        trajectory=VisualTrajectory(),
    )

    piano = VisualizationTrajectoryDescriptor(
        identifier="piano",
        trajectory=VisualTrajectory(),
    )

    scene = ScientificVisualizationScene(
        trajectories=(
            bass,
            piano,
        ),
    )

    selected = scene.select(
        "piano",
    )

    assert selected is piano
