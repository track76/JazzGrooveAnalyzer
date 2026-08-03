from jga.visualization.graphic_scene import (
    GraphicScene,
)

from jga.visualization.scientific_plot_layout import (
    ScientificPlotLayout,
)


def test_scene_accepts_layout():

    layout = ScientificPlotLayout(
        title="Metric Timeline",
        x_axis="time",
        y_axis="metric_position",
    )

    scene = GraphicScene(
        layout=layout,
    )

    assert scene.layout is layout
