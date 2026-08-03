from jga.visualization.scientific_graphic_builder import (
    ScientificGraphicBuilder,
)

from jga.visualization.materialized_plot import (
    MaterializedPlot,
)


def test_scientific_graphic_builder_produces_valid_representation():

    representation = (
        ScientificGraphicBuilder()
        .build(
            MaterializedPlot()
        )
    )

    assert representation.is_valid()
