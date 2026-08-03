from pathlib import Path

from jga.visualization.matplotlib_graphic_renderer import (
    MatplotlibGraphicRenderer,
)

from jga.visualization.graphic_scene import (
    GraphicScene,
)


def test_renderer_output_can_be_saved(
    tmp_path: Path,
):

    output = (
        MatplotlibGraphicRenderer(
            scene=GraphicScene(),
        )
        .render()
    )

    path = tmp_path / "figure.png"

    output.content.savefig(
        path,
    )

    assert path.exists()
