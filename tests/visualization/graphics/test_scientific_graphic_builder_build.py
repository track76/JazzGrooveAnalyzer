from jga.visualization.scientific_graphic_builder import (
    ScientificGraphicBuilder,
)

from jga.visualization.materialized_plot import (
    MaterializedPlot,
)


def test_scientific_graphic_builder_accepts_materialized_plot():

    plot = MaterializedPlot()

    result = (
        ScientificGraphicBuilder()
        .build(plot)
    )

    assert result is not None
