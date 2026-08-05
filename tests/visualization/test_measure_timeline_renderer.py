from jga.visualization.measure_timeline import (
    MeasureTimeline,
)

from jga.visualization.renderers.measure_timeline_matplotlib_renderer import (
    MeasureTimelineMatplotlibRenderer,
)


def test_measure_timeline_renderer_creates_figure():

    timeline = MeasureTimeline(
        measure_number=26,
        beats=(1, 2),
        offsets_ms=(6.4, -9.2),
    )

    figure = (
        MeasureTimelineMatplotlibRenderer()
        .render(timeline)
    )

    assert figure is not None
