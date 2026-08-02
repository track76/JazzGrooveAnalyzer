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


def test_scene_merge():

    scene_a = ScientificVisualizationScene(
        trajectories=(
            descriptor("bass"),
            descriptor("piano"),
        ),
    )

    scene_b = ScientificVisualizationScene(
        trajectories=(
            descriptor("drums"),
        ),
    )

    merged = scene_a.merge(
        scene_b,
    )

    assert merged.identifiers() == (
        "bass",
        "piano",
        "drums",
    )
