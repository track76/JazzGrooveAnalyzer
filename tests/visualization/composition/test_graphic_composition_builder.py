from jga.visualization.scientific_graphic_builder import (
    ScientificGraphicBuilder,
)

from jga.visualization.materialized_plot import (
    MaterializedPlot,
)

from jga.visualization.graphic_composition import (
    GraphicComposition,
)


def test_builder_creates_graphic_composition():

    composition = (
        ScientificGraphicBuilder()
        .compose(
            MaterializedPlot()
        )
    )

    assert isinstance(
        composition,
        GraphicComposition,
    )
