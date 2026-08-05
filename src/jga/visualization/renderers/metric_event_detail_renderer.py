"""
Metric Event Detail Renderer v3.

Renders one metric event microtiming detail.
"""

import matplotlib.pyplot as plt

from jga.visualization.metric_event_detail import (
    MetricEventDetail,
)


class MetricEventDetailRenderer:
    """
    Renders detailed microtiming information
    for one metric event.
    """

    def render(
        self,
        detail: MetricEventDetail,
    ):

        figure, axis = plt.subplots(
            figsize=(8, 3)
        )

        window = max(
            40.0,
            abs(detail.offset_ms) * 5.0,
        )

        # Internal beat reference (0 ms)
        axis.scatter(
            0.0,
            0,
            marker="o",
            facecolors="none",
            s=90,
            linewidths=1.5,
        )

        axis.axvline(
            0.0,
            linewidth=1.0,
        )

        axis.text(
            0.0,
            0.35,
            "Internal Beat",
            ha="center",
        )

        # Observed event
        axis.scatter(
            detail.offset_ms,
            0,
            s=90,
        )

        # Distance from reference
        axis.plot(
            (
                0.0,
                detail.offset_ms,
            ),
            (
                0,
                0,
            ),
        )

        axis.text(
            detail.offset_ms,
            0.18,
            f"{detail.offset_ms:.1f} ms",
            ha="center",
        )

        axis.set_xlim(
            -window,
            window,
        )

        axis.set_ylim(
            -1,
            1,
        )

        axis.set_yticks(
            ()
        )

        axis.set_xlabel(
            "Deviation from internal beat (ms)"
        )

        axis.set_title(
            (
                f"{detail.source_name} | "
                f"Measure {detail.measure_number} | "
                f"Beat {detail.beat_position:.1f}\n"
                f"Offset {detail.offset_ms:.1f} ms "
                f"({detail.deviation_ratio * 100:.2f}% beat)"
            )
        )

        return figure
