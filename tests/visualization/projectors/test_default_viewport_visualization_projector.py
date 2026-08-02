"""
Default Viewport Visualization Projector.

M43.3

Projects one ScientificVisualizationScene into
another by filtering visual points inside one
ScientificVisualizationViewport.

The operation is purely visual.

No scientific meaning is modified.
"""

from jga.visualization.projectors.default_viewport_visualization_projector import (
    DefaultViewportVisualizationProjector,
)
from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
)
from jga.visualization.scientific_visualization_viewport import (
    ScientificVisualizationViewport,
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


def test_projector_filters_points_inside_viewport():

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
                            x=5.0,
                            y=5.0,
                            time=1.0,
                        ),
                        VisualPoint(
                            x=20.0,
                            y=20.0,
                            time=2.0,
                        ),
                    ),
                ),
            ),
        ),
    )

    viewport = ScientificVisualizationViewport(
        x_min=0.0,
        x_max=10.0,
        y_min=0.0,
        y_max=10.0,
    )

    projector = (
        DefaultViewportVisualizationProjector()
    )

    projected = projector.project(
        scene,
        viewport,
    )

    points = (
        projected
        .trajectories[0]
        .trajectory
        .points
    )

    assert len(points) == 2

    assert points[0].x == 0.0
    assert points[1].x == 5.0


def test_projector_preserves_scene_structure():

    scene = ScientificVisualizationScene()

    viewport = ScientificVisualizationViewport(
        x_min=0.0,
        x_max=1.0,
        y_min=0.0,
        y_max=1.0,
    )

    projector = (
        DefaultViewportVisualizationProjector()
    )

    projected = projector.project(
        scene,
        viewport,
    )

    assert isinstance(
        projected,
        ScientificVisualizationScene,
    )
