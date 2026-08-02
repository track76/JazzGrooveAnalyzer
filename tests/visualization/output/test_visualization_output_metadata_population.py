from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
)

from jga.visualization.visualization_trajectory_descriptor import (
    VisualizationTrajectoryDescriptor,
)

from jga.visualization.visual_trajectory import (
    VisualTrajectory,
)

from jga.visualization.visualization_output_builder import (
    VisualizationOutputBuilder,
)


def test_visualization_output_contains_trajectory_count_metadata():

    scene = ScientificVisualizationScene(
        trajectories=(
            VisualizationTrajectoryDescriptor(
                identifier="ensemble",
                trajectory=VisualTrajectory(),
            ),
        ),
    )

    output = (
        VisualizationOutputBuilder()
        .build(scene)
    )

    assert (
        output.metadata["trajectory_count"]
        == 1
    )
