from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
)

from jga.visualization.visualization_trajectory_descriptor import (
    VisualizationTrajectoryDescriptor,
)

from jga.visualization.visual_trajectory import (
    VisualTrajectory,
)


def descriptor(identifier):

    return VisualizationTrajectoryDescriptor(
        identifier=identifier,
        trajectory=VisualTrajectory(),
    )


def test_scene_difference():

    scene_a = ScientificVisualizationScene(
        trajectories=(
            descriptor("bass"),
            descriptor("piano"),
            descriptor("drums"),
        ),
    )

    scene_b = ScientificVisualizationScene(
        trajectories=(
            descriptor("piano"),
        ),
    )

    difference = scene_a.difference(
        scene_b,
    )

    assert difference.identifiers() == (
        "bass",
        "drums",
    )
