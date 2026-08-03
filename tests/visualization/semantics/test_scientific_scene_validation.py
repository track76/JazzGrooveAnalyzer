from jga.visualization.graphic_scene import (
    GraphicScene,
)

from jga.visualization.scientific_plot_metadata import (
    ScientificPlotMetadata,
)


def test_scientific_scene_is_valid():

    scene = GraphicScene(
        scientific_metadata=ScientificPlotMetadata(
            purpose="metric_analysis",
            domain="jazz_rhythm",
        ),
    )

    assert scene.is_valid()
