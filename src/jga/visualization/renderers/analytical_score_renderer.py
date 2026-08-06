
"""
Analytical Score Renderer.

JGA scientific analytical score layout.
"""

import matplotlib.pyplot as plt

from jga.visualization.analytical_score import AnalyticalScore


def _format_time(seconds: float) -> str:
    minutes = int(seconds // 60)
    sec = seconds % 60
    return f"{minutes}:{sec:05.3f}"


class AnalyticalScoreRenderer:

    ORDER = (
        "Trumpet",
        "Piano",
        "Bass",
        "Double Bass",
        "Ride",
        "Hi-Hat",
        "Snare",
        "Kick",
    )

    def render(
        self,
        score: AnalyticalScore,
    ):

        fig, ax = plt.subplots(
            figsize=(16,9)
        )

        measures = score.measures[:4]

        if not measures:
            return fig


        detected = {
            event.source_name
            for measure in measures
            for event in measure.metric_events
        }


        instruments = tuple(
            name
            for name in self.ORDER
            if name in detected
        )


        lanes = {
            name:index
            for index,name in enumerate(instruments)
        }


        beats_per_measure = len(
            measures[0].theoretical_beats
        )


        total_width = (
            len(measures)
            *
            beats_per_measure
        )


        # horizontal lanes

        for y in lanes.values():

            ax.axhline(
                y,
                linewidth=0.4,
                color="lightgray",
                alpha=0.25,
                zorder=0,
            )


        # measure grid

        for m, measure in enumerate(measures):

            start = (
                m
                *
                beats_per_measure
            )


            # measure start/end

            ax.axvline(
                start,
                linewidth=2,
                color="black"
            )


            for beat, x in enumerate(
                measure.beat_positions,
                start=1,
            ):

                x += start


                ax.axvline(
                    x,
                    linestyle=":",
                    linewidth=0.7,
                    color="gray"
                )


                ax.text(
                    x,
                    1.08,
                    str(beat),
                    ha="center",
                    transform=ax.get_xaxis_transform()
                )


                ax.text(
                    x,
                    1.03,
                    f"{measure.bpm:.1f}",
                    ha="center",
                    fontsize=8,
                    transform=ax.get_xaxis_transform()
                )


            ax.axvline(
                start + beats_per_measure,
                linewidth=2,
                color="black"
            )


            ax.text(
                start + beats_per_measure/2,
                1.18,
                str(measure.number),
                ha="center",
                fontsize=14,
                transform=ax.get_xaxis_transform()
            )


        # events

        for m, measure in enumerate(measures):

            for event in measure.metric_events:

                name = event.source_name

                if name == "Double Bass":
                    name = "Bass"

                if name not in lanes:
                    continue


                x = (
                    m * beats_per_measure
                    +
                    event.beat_index
                )


                y = lanes[name]


                marker = "x" if name in (
                    "Hi-Hat",
                ) else "o"


                ax.scatter(
                    x,
                    y,
                    marker=marker,
                    s=42,
                    color="black",
                    linewidths=1.0,
                    zorder=3,
                )


                if event.offset_ms:

                    ax.text(
                        x,
                        y+0.12,
                        f"{event.offset_ms:.1f} ms",
                        fontsize=8,
                        ha="center"
                    )


        ax.set_xlim(
            -0.05,
            total_width+0.05
        )


        ax.set_yticks(
            list(lanes.values())
        )

        ax.set_yticklabels(
            list(lanes.keys())
        )


        ax.set_xticks([])


        ax.set_title(
            (
                "JGA Analytical Groove Score\n"
                f"{score.recording_title}\n"
                f"{score.time_signature} | "
                f"Average BPM {score.average_bpm:.1f}"
            ),
            fontsize=18,
            pad=35
        )


        ax.set_ylabel(
            "Instrument"
        )


        fig.subplots_adjust(
            top=0.82,
            bottom=0.15,
            left=0.12,
            right=0.98
        )


        return fig
