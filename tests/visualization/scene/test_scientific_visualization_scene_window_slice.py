from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
)

from jga.visualization.temporal_visualization_window import (
    TemporalVisualizationWindow,
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


def test_scene_slice_with_window():

    scene = ScientificVisualizationScene(
        trajectories=(
            VisualizationTrajectoryDescriptor(
                identifier="ensemble",
                trajectory=VisualTrajectory(
                    points=(
                        VisualPoint(
                            x=0.0,
                            y=0.0,
                            time=10.0,
                        ),
                        VisualPoint(
                            x=1.0,
                            y=1.0,
                            time=20.0,
                        ),
                    ),
                ),
            ),
        ),
    )

    window = TemporalVisualizationWindow(
        start_time=15.0,
        end_time=25.0,
    )

    sliced = scene.slice(
        window,
    )

    assert (
        sliced.total_points()
        == 1
    )
