from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
)

from jga.visualization.visual_trajectory import (
    VisualTrajectory,
)

from jga.visualization.visual_point import (
    VisualPoint,
)

from jga.visualization.visual_trajectory_scene_adapter import (
    VisualTrajectorySceneAdapter,
)


def test_adapter_creates_scene():

    trajectory = VisualTrajectory(
        points=(
            VisualPoint(
                x=1.0,
                y=2.0,
                time=3.0,
            ),
        ),
    )

    scene = (
        VisualTrajectorySceneAdapter()
        .adapt(
            trajectory,
            identifier="ensemble",
        )
    )

    assert isinstance(
        scene,
        ScientificVisualizationScene,
    )

    assert (
        scene.trajectories[0].identifier
        == "ensemble"
    )
