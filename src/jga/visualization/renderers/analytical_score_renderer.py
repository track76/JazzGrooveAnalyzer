"""
Analytical Score Renderer.

Complete analytical groove representation.

Shows:
- measures
- beat grid
- BPM
- real musical time
- metric events
"""

import matplotlib.pyplot as plt

from jga.visualization.analytical_score import (
    AnalyticalScore,
)


def _format_time(seconds: float) -> str:
    minutes = int(seconds // 60)
    remainder = seconds % 60
    return f"{minutes}:{remainder:06.3f}"


class AnalyticalScoreRenderer:
    """
    Renders complete analytical score.
    """

    def render(
        self,
        score: AnalyticalScore,
    ):

        figure, axis = plt.subplots(
            figsize=(16, 9)
        )

        figure.subplots_adjust(
            top=0.78,
            bottom=0.18,
        )

        measures = score.measures[:4]

        if not measures:
            return figure

        instruments = tuple(
            dict.fromkeys(
                event.source_name
                for measure in measures
                for event in measure.metric_events
            )
        )

        instrument_y = {
            name: index
            for index, name in enumerate(instruments)
        }

        # instrument lanes
        for y in instrument_y.values():
            axis.axhline(
                y,
                linewidth=0.6,
                linestyle="--",
                alpha=0.5,
            )

        beats_per_measure = len(
            measures[0].theoretical_beats
        )

        total_beats = (
            len(measures)
            *
            beats_per_measure
        )

        # -------------------------
        # Measures and beat grid
        # -------------------------

        for measure_index, measure in enumerate(measures):

            measure_start = (
                measure_index
                *
                beats_per_measure
            )

            seconds_per_beat = (
                60.0 / measure.bpm
            )

            # measure bar
            axis.axvline(
                measure_start,
                linewidth=2.8,
            )

            # four cells in 4/4
            for beat in range(
                beats_per_measure
            ):

                beat_center = (
                    measure_start
                    +
                    beat
                    +
                    0.5
                )

                # internal beat line
                axis.axvline(
                    beat_center,
                    linewidth=0.6,
                    linestyle=":",
                    alpha=0.7,
                )

                # beat number
                axis.text(
                    beat_center,
                    1.10,
                    str(beat + 1),
                    ha="center",
                    va="bottom",
                    transform=axis.get_xaxis_transform(),
                )

                # bpm
                axis.text(
                    beat_center,
                    1.04,
                    f"BPM {measure.bpm:.1f}",
                    ha="center",
                    va="bottom",
                    fontsize=8,
                    transform=axis.get_xaxis_transform(),
                )

                # real time
                axis.text(
                    beat_center,
                    -0.18,
                    _format_time(
                        measure.start_time_seconds
                        +
                        (
                            beat
                            *
                            seconds_per_beat
                        )
                    ),
                    ha="center",
                    va="top",
                    fontsize=8,
                    transform=axis.get_xaxis_transform(),
                )

            # measure end bar
            axis.axvline(
                measure_start + beats_per_measure,
                linewidth=2.8,
            )



        # separator between harmonic instruments and drums
        if instrument_y:
            axis.axhline(
                len(instrument_y) - 1.5,
                linewidth=1.0,
                color="black",
                alpha=0.8,
            )

        # -------------------------
        # Events
        # -------------------------

        for measure_index, measure in enumerate(measures):

            seconds_per_beat = (
                60.0 / measure.bpm
            )

            for event in measure.metric_events:

                if event.source_name not in instrument_y:
                    continue

                y = instrument_y[
                    event.source_name
                ]

                x = (
                    measure_index
                    *
                    beats_per_measure
                    +
                    event.beat_index
                    +
                    1
                    +
                    (
                        event.offset_ms
                        /
                        1000.0
                        /
                        seconds_per_beat
                    )
                )

                if event.source_name.lower() in (
                    "hi-hat",
                    "hihat",
                    "hi_hat",
                ):

                    axis.scatter(
                        x,
                        y,
                        marker="x",
                        s=50,
                    )

                elif event.source_name.lower() in (
                    "ride",
                    "snare",
                    "kick",
                    "bass drum",
                ):

                    axis.scatter(
                        x,
                        y,
                        marker="o",
                        s=50,
                    )

                else:

                    axis.scatter(
                        x,
                        y,
                        marker="o",
                        s=70,
                    )

                if event.offset_ms != 0.0:

                    axis.text(
                        x + 0.02,
                        y + 0.08,
                        f"{event.offset_ms:.1f} ms",
                    )

        # -------------------------
        # Labels
        # -------------------------

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

        # hide automatic metric axis
        axis.set_xticks([])

        axis.set_xlabel(
            ""
        )

        axis.set_ylabel(
            "Instrument"
        )

        axis.set_xlim(
            -0.2,
            len(measures) * 4 + 0.2
        )

        # title separated from annotations
        axis.set_title(
            (
                f"{score.recording_title}\n"
                f"Analytical Groove Score\n"
                f"{score.time_signature} | "
                f"Average BPM {score.average_bpm:.1f}"
            ),
            pad=45,
        )

        axis.set_ylim(
            -0.15,
            len(instruments) - 0.85
        )

        # measure information
        for measure_index, measure in enumerate(measures):

            measure_position = (
                measure_index
                *
                beats_per_measure
            )

            axis.text(
                measure_position,
                1.04,
                (
                    f"{measure.number}\n"
                    f"BPM {measure.bpm:.1f}"
                ),
                ha="left",
                va="bottom",
                transform=axis.get_xaxis_transform(),
            )

            axis.text(
                measure_position,
                -0.12,
                _format_time(
                    measure.start_time_seconds
                ),
                ha="center",
                va="top",
                transform=axis.get_xaxis_transform(),
                fontsize=9,
            )

        figure.subplots_adjust(
            top=0.88,
            bottom=0.12,
        )

        return figure
