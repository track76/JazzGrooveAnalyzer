"""
Ensemble Microtiming Renderer.

Renders collective temporal behaviour
of an ensemble at one metric position.
"""

import matplotlib.pyplot as plt

from jga.visualization.ensemble_microtiming_profile import (
    EnsembleMicrotimingProfile,
)


class EnsembleMicrotimingRenderer:
    """
    Renders ensemble microtiming profile.
    """

    def render(
        self,
        profile: EnsembleMicrotimingProfile,
    ):

        figure, axis = plt.subplots(
            figsize=(9, 5)
        )

        instruments = tuple(
            event.source_name
            for event in profile.events
        )

        y_positions = {
            name: index
            for index, name
            in enumerate(instruments)
        }

        offsets = tuple(
            event.offset_ms
            for event in profile.events
        )

        window = max(
            40.0,
            max(
                abs(offset)
                for offset
                in offsets
            )
            * 5.0,
        )

        # Vertical microtiming grid
        for value in range(
            int(-window),
            int(window) + 1,
            10,
        ):

            axis.axvline(
                value,
                linewidth=0.5,
                linestyle="--",
            )

        # Internal beat reference
        axis.axvline(
            0.0,
            linewidth=1.2,
        )

        # Instrument lanes
        for y in y_positions.values():

            axis.axhline(
                y,
                linewidth=0.5,
            )

        for event in profile.events:

            y = y_positions[
                event.source_name
            ]

            axis.scatter(
                event.offset_ms,
                y,
                s=80,
            )

            if event.offset_ms < 0:

                label_x = event.offset_ms - 1.5
                alignment = "right"

            else:

                label_x = event.offset_ms + 1.5
                alignment = "left"

            axis.text(
                label_x,
                y + 0.12,
                f"{event.offset_ms:.1f} ms",
                ha=alignment,
                va="center",
            )

        axis.set_yticks(
            tuple(
                y_positions.values()
            )
        )

        axis.set_yticklabels(
            tuple(
                y_positions.keys()
            )
        )

        axis.set_xlim(
            -window,
            window,
        )

        axis.set_ylim(
            -0.5,
            len(instruments) - 0.5,
        )

        axis.set_xlabel(
            "Deviation from internal beat (ms)"
        )

        axis.set_title(
            (
                f"Ensemble Microtiming "
                f"- Measure {profile.measure_number} "
                f"- Beat {profile.beat_position}"
            )
        )

        figure.tight_layout()

        return figure
