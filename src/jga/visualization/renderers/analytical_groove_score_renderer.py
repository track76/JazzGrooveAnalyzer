"""
Analytical Groove Score Renderer v2.

Renders:
- internal metric grid
- theoretical metric positions
- observed events
- temporal displacement
"""

import matplotlib.pyplot as plt

from jga.visualization.measure import Measure


class AnalyticalGrooveScoreRenderer:
    """
    Renders one measure as an analytical groove score.
    """

    def render(
        self,
        measure: Measure,
    ):

        figure, axis = plt.subplots(
            figsize=(10, 5)
        )

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

        # Internal metric grid
        for beat in measure.theoretical_beats:

            axis.axvline(
                beat,
                linewidth=0.8,
            )

        # Events
        for event in measure.metric_events:

            y = instrument_y[
                event.source_name
            ]

            # theoretical position
            axis.scatter(
                event.theoretical_position,
                y,
            )

            # observed position
            axis.scatter(
                event.beat_index,
                y,
            )

            # deviation line
            axis.plot(
                (
                    event.theoretical_position,
                    event.beat_index,
                ),
                (
                    y,
                    y,
                ),
            )

            if event.offset_ms != 0.0:

                axis.text(
                    event.beat_index,
                    y + 0.08,
                    f"{event.offset_ms:.1f} ms",
                )

        axis.set_title(
            f"Analytical Groove Score "
            f"- Measure {measure.number} "
            f"- Metric reference {measure.bpm:.1f} "
            f"{measure.metric_reference_beat_unit} BPM "
            f"({measure.metric_reference_origin})"
        )

        axis.set_xlabel(
            "Metric position"
        )

        axis.set_ylabel(
            "Instrument"
        )

        axis.set_yticks(
            tuple(
                instrument_y.values()
            )
        )

        axis.set_yticklabels(
            tuple(
                instrument_y.keys()
            )
        )

        axis.set_xticks(
            measure.theoretical_beats
        )

        axis.set_xlim(
            0.5,
            max(measure.theoretical_beats) + 0.5,
        )

        return figure
