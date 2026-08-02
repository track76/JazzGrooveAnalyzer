import pytest

from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
)

from jga.visualization.visualization_trajectory_descriptor import (
    VisualizationTrajectoryDescriptor,
)

from jga.visualization.visual_trajectory import (
    VisualTrajectory,
)


def test_scene_raises_for_unknown_identifier():

    scene = ScientificVisualizationScene(
        trajectories=(
            VisualizationTrajectoryDescriptor(
                identifier="bass",
                trajectory=VisualTrajectory(),
            ),
        ),
    )

    with pytest.raises(
        ValueError,
    ):
        scene.select(
            "piano",
        )
