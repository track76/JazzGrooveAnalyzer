from jga.visualization.pipeline.visualization_projection_pipeline import (
    VisualizationProjectionPipeline,
)

from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
)

from jga.visualization.visualization_trajectory_descriptor import (
    VisualizationTrajectoryDescriptor,
)

from jga.visualization.visual_trajectory import (
    VisualTrajectory,
)


def descriptor(
    identifier: str,
):
    return VisualizationTrajectoryDescriptor(
        identifier=identifier,
        trajectory=VisualTrajectory(),
    )


def test_comparative_projection_preserves_sources():

    scene = ScientificVisualizationScene(
        trajectories=(
            descriptor("bass"),
            descriptor("piano"),
        ),
    )

    projected = (
        VisualizationProjectionPipeline()
        .project(
            scene,
        )
    )

    assert projected.contains(
        "bass"
    )

    assert projected.contains(
        "piano"
    )
