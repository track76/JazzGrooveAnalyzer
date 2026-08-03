from jga.visualization.graphic_representation import (
    GraphicRepresentation,
)

from jga.visualization.materialized_plot import (
    MaterializedPlot,
)

from jga.visualization.line_element import (
    LineElement,
)


def test_graphic_representation_supports_multiple_elements():

    first = LineElement(
        points=(
            (0.0, 0.0),
            (1.0, 1.0),
        ),
    )

    second = LineElement(
        points=(
            (1.0, 0.0),
            (0.0, 1.0),
        ),
    )

    representation = GraphicRepresentation(
        source_plot=MaterializedPlot(),
        elements=(
            first,
            second,
        ),
    )

    assert len(
        representation.elements
    ) == 2
