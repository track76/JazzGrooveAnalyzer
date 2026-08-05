"""
Measure Timeline Matplotlib Renderer.

Renders metric displacement inside one measure.
"""

import matplotlib.pyplot as plt

from jga.visualization.measure_timeline import (
    MeasureTimeline,
)


class MeasureTimelineMatplotlibRenderer:
    """
    Renders one measure groove timeline.
    """

    def render(
        self,
        timeline: MeasureTimeline,
    ):

        figure, axis = plt.subplots()

        axis.axhline(
            0,
        )

        axis.scatter(
            timeline.beats,
            timeline.offsets_ms,
        )

        axis.set_title(
            f"Measure {timeline.measure_number}"
        )

        axis.set_xlabel(
            "Beat"
        )

        axis.set_ylabel(
            "Offset (ms)"
        )

        axis.set_xticks(
            (1, 2, 3, 4)
        )

        return figure
