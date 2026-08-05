"""
Analytical Groove Score Renderer v3.

Two-level analytical representation:

1. Metric position
   - internal beat grid
   - theoretical position
   - observed events

2. Microtiming deviation
   - temporal displacement in milliseconds
"""

import matplotlib.pyplot as plt

from jga.visualization.measure import Measure


class AnalyticalGrooveScoreV3Renderer:
    """
    Renders metric position and microtiming deviation.
    """

    def render(
        self,
        measure: Measure,
    ):

        figure, axes = plt.subplots(
            2,
            1,
            figsize=(10, 8),
            sharex=True,
            gridspec_kw={
                "height_ratios": (2, 1)
            },
        )

        metric_axis, timing_axis = axes

        instruments = tuple(
            dict.fromkeys(
                event.source_name
                for event in measure.metric_events
            )
        )

        instrument_y = {
            name: index
            for index, name
            in enumerate(instruments)
        }

        # -------------------------
        # Metric position view
        # -------------------------

        for beat in measure.theoretical_beats:
            metric_axis.axvline(
                beat,
                linewidth=0.8,
            )

        for event in measure.metric_events:

            y = instrument_y[
                event.source_name
            ]

            metric_axis.scatter(
                event.theoretical_position,
                y,
            )

            metric_axis.scatter(
                event.beat_index,
                y,
            )

            metric_axis.plot(
                (
                    event.theoretical_position,
                    event.beat_index,
                ),
                (
                    y,
                    y,
                ),
            )

        metric_axis.set_yticks(
            tuple(
                instrument_y.values()
            )
        )

        metric_axis.set_yticklabels(
            tuple(
                instrument_y.keys()
            )
        )

        metric_axis.set_ylabel(
            "Instrument"
        )

        metric_axis.set_title(
            f"Analytical Groove Score "
            f"- Measure {measure.number} "
            f"- BPM {measure.bpm:.1f}"
        )

        # -------------------------
        # Microtiming view
        # -------------------------

        for beat in measure.theoretical_beats:
            timing_axis.axvline(
                beat,
                linewidth=0.8,
            )

        for event in measure.metric_events:

            y = 0

            timing_axis.scatter(
                event.beat_index,
                event.offset_ms,
            )

        timing_axis.axhline(
            0,
            linewidth=1.0,
        )

        timing_axis.set_ylim(
            -20,
            20,
        )

        timing_axis.set_ylabel(
            "Offset (ms)"
        )

        timing_axis.set_xlabel(
            "Metric position"
        )

        timing_axis.set_xticks(
            measure.theoretical_beats
        )

        metric_axis.set_xlim(
            0.5,
            max(measure.theoretical_beats) + 0.5,
        )

        return figure
