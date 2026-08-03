from jga.visualization.scientific_graphic_builder import (
    ScientificGraphicBuilder,
)

from jga.visualization.materialized_plot import (
    MaterializedPlot,
)

from jga.visualization.graphic_scene import (
    GraphicScene,
)


def test_builder_creates_graphic_scene():

    scene = (
        ScientificGraphicBuilder()
        .scene(
            MaterializedPlot()
        )
    )

    assert isinstance(
        scene,
        GraphicScene,
    )
