from jga.visualization.scientific_graphic_builder import (
    ScientificGraphicBuilder,
)

from jga.visualization.materialized_plot import (
    MaterializedPlot,
)


def test_graphic_representation_keeps_source_plot():

    plot = MaterializedPlot()

    representation = (
        ScientificGraphicBuilder()
        .build(plot)
    )

    assert representation.source_plot is plot
