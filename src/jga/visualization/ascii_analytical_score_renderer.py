"""
ASCII Analytical Score Renderer.

Prototype renderer used to validate the logical layout of the
Analytical Score before graphical rendering.
"""

from jga.visualization.analytical_score import (
    AnalyticalScore,
)


class AsciiAnalyticalScoreRenderer:

    def render(
        self,
        score: AnalyticalScore,
    ) -> str:

        lines = []

        lines.append("=" * 70)
        lines.append("Jazz Groove Analyzer")
        lines.append("")
        lines.append(f"Title : {score.recording_title}")
        lines.append(f"Artist: {score.artist}")
        lines.append(f"Meter : {score.time_signature}")
        lines.append(f"Tempo : {score.average_bpm:.1f} BPM")
        lines.append("=" * 70)
        lines.append("")

        lines.append("FORM")

        if score.sections:
            lines.append(
                " | ".join(
                    section.name
                    for section in score.sections
                )
            )
        else:
            lines.append("(none)")

        lines.append("")
        lines.append("=" * 70)
        lines.append("")

        lines.append("MEASURES")

        if score.measures:
            measure_line = " ".join(
                f"[{m.number}]"
                for m in score.measures
            )
            lines.append(measure_line)

            beat_line = " ".join(
                "|1|2|3|4|"
                for _ in score.measures
            )
            lines.append(beat_line)

        lines.append("")
        lines.append("=" * 70)
        lines.append("")

        lines.append("INSTRUMENTS")

        for lane in score.instrument_lanes:
            lines.append(f"{lane.name:<12}")

        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)
