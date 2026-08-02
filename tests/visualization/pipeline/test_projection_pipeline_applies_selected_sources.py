from jga.visualization.pipeline.visualization_projection_pipeline import (
    VisualizationProjectionPipeline,
)

from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
)

from jga.visualization.visualization_state import (
    VisualizationState,
)

from jga.visualization.visualization_trajectory_descriptor import (
    VisualizationTrajectoryDescriptor,
)

from jga.visualization.visual_trajectory import (
    VisualTrajectory,
)


def test_projection_pipeline_applies_selected_sources():

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

    state = VisualizationState(
        selected_sources=(
            "bass",
        ),
    )

    projected = (
        VisualizationProjectionPipeline()
        .project(
            scene,
            state=state,
        )
    )

    assert projected.identifiers() == (
        "bass",
    )
