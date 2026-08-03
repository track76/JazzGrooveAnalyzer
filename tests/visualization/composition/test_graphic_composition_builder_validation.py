from jga.visualization.scientific_graphic_builder import (
    ScientificGraphicBuilder,
)

from jga.visualization.materialized_plot import (
    MaterializedPlot,
)


def test_builder_creates_valid_composition():

    composition = (
        ScientificGraphicBuilder()
        .compose(
            MaterializedPlot()
        )
    )

    assert composition.is_valid()
