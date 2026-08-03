from jga.visualization.scientific_graphic_builder import (
    ScientificGraphicBuilder,
)

from jga.visualization.materialized_plot import (
    MaterializedPlot,
)


def test_builder_creates_valid_scene():

    scene = (
        ScientificGraphicBuilder()
        .scene(
            MaterializedPlot()
        )
    )

    assert scene.is_valid()

    assert len(
        scene.compositions
    ) > 0
