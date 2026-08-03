from jga.visualization.graphic_scene import (
    GraphicScene,
)

from jga.visualization.graphic_composition import (
    GraphicComposition,
)

from jga.visualization.scientific_plot_metadata import (
    ScientificPlotMetadata,
)


def test_scene_semantics_with_composition():

    composition = GraphicComposition()

    scene = GraphicScene(
        compositions=(
            composition,
        ),
        scientific_metadata=ScientificPlotMetadata(
            purpose="metric_analysis",
            domain="jazz_rhythm",
        ),
    )

    assert scene.compositions[0] is composition
