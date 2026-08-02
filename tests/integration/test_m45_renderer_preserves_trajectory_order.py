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


def descriptor(identifier, y):

    return VisualizationTrajectoryDescriptor(
        identifier=identifier,
        trajectory=VisualTrajectory(
            points=(
                VisualPoint(
                    x=0.0,
                    y=y,
                    time=0.0,
                ),
                VisualPoint(
                    x=1.0,
                    y=y,
                    time=1.0,
                ),
            ),
        ),
    )


def test_renderer_preserves_trajectory_order():

    scene = ScientificVisualizationScene(
        trajectories=(
            descriptor("bass", 0.0),
            descriptor("piano", 10.0),
            descriptor("drums", 20.0),
        ),
    )

    figure = (
        MatplotlibRenderer()
        .render_scene(
            scene,
        )
    )

    axes = figure.axes[0]

    labels = [
        line.get_label()
        for line in axes.lines
    ]

    assert labels == [
        "bass",
        "piano",
        "drums",
    ]
