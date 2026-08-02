from jga.visualization.renderers.matplotlib_renderer import (
    MatplotlibRenderer,
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

from jga.visualization.visual_point import (
    VisualPoint,
)


def trajectory(identifier, y):

    return VisualizationTrajectoryDescriptor(
        identifier=identifier,
        trajectory=VisualTrajectory(
            points=(
                VisualPoint(x=0.0, y=y, time=0.0),
                VisualPoint(x=1.0, y=y, time=1.0),
                VisualPoint(x=2.0, y=y, time=2.0),
            ),
        ),
    )


def test_renderer_renders_multiple_trajectories():

    scene = ScientificVisualizationScene(
        trajectories=(
            trajectory("bass", 0.0),
            trajectory("piano", 5.0),
            trajectory("drums", -5.0),
        ),
    )

    figure = (
        MatplotlibRenderer()
        .render_scene(
            scene,
        )
    )

    assert figure is not None

    axes = figure.axes[0]

    assert len(
        axes.lines
    ) == 3
