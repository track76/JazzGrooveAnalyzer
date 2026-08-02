from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
)

from jga.visualization.visualization_trajectory_descriptor import (
    VisualizationTrajectoryDescriptor,
)

from jga.visualization.visual_trajectory import (
    VisualTrajectory,
)


def test_scene_filters_selected_trajectories():

    bass = VisualizationTrajectoryDescriptor(
        identifier="bass",
        trajectory=VisualTrajectory(),
    )

    piano = VisualizationTrajectoryDescriptor(
        identifier="piano",
        trajectory=VisualTrajectory(),
    )

    drums = VisualizationTrajectoryDescriptor(
        identifier="drums",
        trajectory=VisualTrajectory(),
    )

    scene = ScientificVisualizationScene(
        trajectories=(
            bass,
            piano,
            drums,
        ),
    )

    filtered = scene.filter(
        "bass",
        "drums",
    )

    assert filtered.identifiers() == (
        "bass",
        "drums",
    )
