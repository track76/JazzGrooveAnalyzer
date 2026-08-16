"""
Analytical Groove Score Renderer.

Multi-panel temporal representation.
"""

import matplotlib.pyplot as plt

from collections import defaultdict
from matplotlib.ticker import FuncFormatter

from jga.visualization.measure import Measure
from jga.visualization.measure_block import MeasureBlock


def _instrument_priority(name: str) -> int:
    order = {
        "Trumpet": 0,
        "Piano": 1,
        "Bass": 2,
        "Ride": 3,
        "Hi-Hat": 4,
        "Snare": 5,
        "Kick": 6,
    }

    return order.get(name, 99)


class AnalyticalGrooveScoreV3Renderer:


    def render(
        self,
        measure: Measure | MeasureBlock,
    ):

        if isinstance(measure, MeasureBlock):
            measures = measure.measures
        else:
            measures = (measure,)

        figure, axis = plt.subplots(
            figsize=(14, 8)
        )

        instruments = tuple(
            sorted(
                {
                    event.source_name
                    for m in measures
                    for event in m.metric_events
                },
                key=_instrument_priority,
            )
        )

        instrument_y = {
            name: index
            for index, name
            in enumerate(reversed(instruments))
        }

        for y in instrument_y.values():

            axis.axhline(
                y,
                linewidth=0.5,
            )

        for m in measures:

            # measure boundary
            axis.axvline(
                m.start_time_seconds,
                linewidth=2.0,
            )

            # quarter-note beats only
            # derived from the actual measure timeline,
            # not from subdivision count.

            measure_duration = (
                m.beat_positions[-1]
                -
                m.beat_positions[0]
            )

            beat_duration = (
                measure_duration
                /
                4
            )

            for beat_index in range(4):

                axis.axvline(
                    m.start_time_seconds
                    +
                    beat_index * beat_duration,
                    linestyle="--",
                    linewidth=1.2,
                )

            event_offsets = defaultdict(int)

            for event in m.metric_events:

                base_y = instrument_y[
                    event.source_name
                ]

                offset = (
                    event_offsets[
                        event.source_name
                    ]
                    %
                    5
                ) * 0.08

                event_offsets[
                    event.source_name
                ] += 1

                axis.scatter(
                    event.absolute_time_seconds,
                    base_y + offset,
                    s=12,
                )

            axis.text(
                m.start_time_seconds,
                len(instruments) + 0.3,
                f"M{m.number}",
                fontsize=12,
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

        axis.set_ylabel(
            "Instrument"
        )

        axis.set_xlabel(
            "Time (mm:ss.xxx)"
        )

        axis.xaxis.set_major_formatter(
            FuncFormatter(
                lambda x, pos:
                f"{int(x//60):02d}:{x%60:06.3f}"
            )
        )

        axis.set_title(
            f"Analytical Groove Score "
            f"- Measures "
            f"{measures[0].number}-{measures[-1].number}"
            f" - Metric reference {measures[0].bpm:.1f} "
            f"{measures[0].metric_reference_beat_unit} BPM "
            f"({measures[0].metric_reference_origin})"
        )

        last_measure = measures[-1]

        measure_duration = (
            last_measure.beat_positions[-1]
            -
            last_measure.beat_positions[0]
        )

        axis.set_xlim(
            measures[0].start_time_seconds,
            last_measure.start_time_seconds
            +
            measure_duration
            +
            0.1,
        )

        return figure
