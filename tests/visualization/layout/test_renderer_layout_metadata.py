from jga.visualization.graphic_scene import (
    GraphicScene,
)

from jga.visualization.matplotlib_graphic_renderer import (
    MatplotlibGraphicRenderer,
)

from jga.visualization.scientific_plot_layout import (
    ScientificPlotLayout,
)


def test_renderer_preserves_layout():

    scene = GraphicScene(
        layout=ScientificPlotLayout(
            title="Metric Timeline",
            x_axis="time",
            y_axis="metric_position",
        ),
    )

    output = (
        MatplotlibGraphicRenderer(
            scene=scene,
        )
        .render()
    )

    assert output.metadata["renderer"] == "matplotlib"
