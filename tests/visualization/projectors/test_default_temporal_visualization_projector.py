from jga.visualization.projectors.default_temporal_visualization_projector import (
    DefaultTemporalVisualizationProjector,
)
from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
)
from jga.visualization.temporal_visualization_window import (
    TemporalVisualizationWindow,
)
from jga.visualization.visual_point import (
    VisualPoint,
)
from jga.visualization.visual_trajectory import (
    VisualTrajectory,
)
from jga.visualization.visualization_trajectory_descriptor import (
    VisualizationTrajectoryDescriptor,
)


def test_projector_filters_points_outside_window():

    scene = ScientificVisualizationScene(
        trajectories=(
            VisualizationTrajectoryDescriptor(
                identifier="bass",
                trajectory=VisualTrajectory(
                    points=(
                        VisualPoint(
                            x=0.0,
                            y=0.0,
                            time=0.0,
                        ),
                        VisualPoint(
                            x=1.0,
                            y=1.0,
                            time=1.0,
                        ),
                        VisualPoint(
                            x=2.0,
                            y=2.0,
                            time=2.0,
                        ),
                    ),
                ),
            ),
        ),
    )

    window = TemporalVisualizationWindow(
        start_time=0.5,
        end_time=1.5,
    )

    projector = DefaultTemporalVisualizationProjector()

    projected = projector.project(
        scene,
        window,
    )

    points = (
        projected.trajectories[0]
        .trajectory
        .points
    )

    assert len(points) == 1
    assert points[0].time == 1.0
