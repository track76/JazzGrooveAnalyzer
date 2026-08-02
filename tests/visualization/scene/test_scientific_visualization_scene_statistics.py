from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
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


def trajectory(identifier, count):

    return VisualizationTrajectoryDescriptor(
        identifier=identifier,
        trajectory=VisualTrajectory(
            points=tuple(
                VisualPoint(
                    x=float(i),
                    y=0.0,
                    time=float(i),
                )
                for i in range(count)
            ),
        ),
    )


def test_scene_reports_statistics():

    scene = ScientificVisualizationScene(
        trajectories=(
            trajectory("bass", 10),
            trajectory("piano", 20),
            trajectory("drums", 30),
        ),
    )

    assert scene.trajectory_count() == 3

    assert scene.total_points() == 60
