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


def test_renderer_ignores_empty_trajectories():

    scene = ScientificVisualizationScene(
        trajectories=(
            VisualizationTrajectoryDescriptor(
                identifier="empty",
                trajectory=VisualTrajectory(),
            ),
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
                            y=0.0,
                            time=1.0,
                        ),
                    ),
                ),
            ),
        ),
    )

    figure = (
        MatplotlibRenderer()
        .render_scene(
            scene,
        )
    )

    axes = figure.axes[0]

    assert len(
        axes.lines
    ) == 1

    assert (
        axes.lines[0].get_label()
        == "bass"
    )
