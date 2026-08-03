from jga.visualization.matplotlib_graphic_renderer import (
    MatplotlibGraphicRenderer,
)

from jga.visualization.graphic_scene import (
    GraphicScene,
)

from jga.visualization.scientific_plot_metadata import (
    ScientificPlotMetadata,
)


def test_output_contains_scientific_metadata():

    scene = GraphicScene(
        scientific_metadata=ScientificPlotMetadata(
            purpose="metric_analysis",
            domain="jazz_rhythm",
        ),
    )

    output = (
        MatplotlibGraphicRenderer(
            scene=scene,
        )
        .render()
    )

    assert output.metadata["renderer"] == "matplotlib"
