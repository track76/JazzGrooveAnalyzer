from jga.visualization.pipeline.visualization_projection_pipeline import (
    VisualizationProjectionPipeline,
)

from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
)

from jga.visualization.temporal_visualization_window import (
    TemporalVisualizationWindow,
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

from jga.visualization.visual_point import (
    VisualPoint,
)


def test_projection_pipeline_applies_state_temporal_window():

    scene = ScientificVisualizationScene(
        trajectories=(
            VisualizationTrajectoryDescriptor(
                identifier="ensemble",
                trajectory=VisualTrajectory(
                    points=(
                        VisualPoint(
                            x=0.0,
                            y=0.0,
                            time=5.0,
                        ),
                        VisualPoint(
                            x=1.0,
                            y=1.0,
                            time=15.0,
                        ),
                    ),
                ),
            ),
        ),
    )

    state = VisualizationState(
        temporal_window=TemporalVisualizationWindow(
            start_time=10.0,
            end_time=20.0,
        ),
    )

    projected = (
        VisualizationProjectionPipeline()
        .project(
            scene,
            state=state,
        )
    )

    assert projected.total_points() == 1
