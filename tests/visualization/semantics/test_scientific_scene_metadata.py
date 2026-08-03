from jga.visualization.graphic_scene import (
    GraphicScene,
)

from jga.visualization.scientific_plot_metadata import (
    ScientificPlotMetadata,
)


def test_scene_accepts_scientific_metadata():

    metadata = ScientificPlotMetadata(
        purpose="metric_analysis",
        domain="jazz_rhythm",
    )

    scene = GraphicScene(
        scientific_metadata=metadata,
    )

    assert scene.scientific_metadata is metadata
