import matplotlib.figure

from jga.visualization.renderers.multi_trajectory_renderer import (
    MultiTrajectoryRenderer,
)
from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
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


def test_multi_trajectory_renderer_creates_figure():

    scene = ScientificVisualizationScene(
        trajectories=(
            VisualizationTrajectoryDescriptor(
                identifier="bass",
                trajectory=VisualTrajectory(
                    points=(
                        VisualPoint(
                            x=0.0,
                            y=1.0,
                            time=0.0,
                        ),
                    ),
                ),
            ),
            VisualizationTrajectoryDescriptor(
                identifier="drums",
                trajectory=VisualTrajectory(
                    points=(
                        VisualPoint(
                            x=0.0,
                            y=-1.0,
                            time=0.0,
                        ),
                    ),
                ),
            ),
        ),
    )

    renderer = MultiTrajectoryRenderer()

    figure = renderer.render(scene)

    assert isinstance(
        figure,
        matplotlib.figure.Figure,
    )
