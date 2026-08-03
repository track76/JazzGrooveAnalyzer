from jga.visualization.scientific_graphic_builder import (
    ScientificGraphicBuilder,
)

from jga.visualization.materialized_plot import (
    MaterializedPlot,
)

from jga.visualization.matplotlib_graphic_renderer import (
    MatplotlibGraphicRenderer,
)


def test_full_render_pipeline():

    scene = (
        ScientificGraphicBuilder()
        .scene(
            MaterializedPlot()
        )
    )

    output = (
        MatplotlibGraphicRenderer(
            scene=scene,
        )
        .render()
    )

    assert output.content is not None
