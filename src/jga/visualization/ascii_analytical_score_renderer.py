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
        if score.metric_reference_origin is not None:
            lines.append(
                "Metric reference "
                f"({score.metric_reference_origin}) : "
                f"{score.average_bpm:.1f} "
                f"{score.metric_reference_beat_unit} BPM"
            )
            lines.append(
                f"Metric reference source: {score.metric_reference_source_id}"
            )
        else:
            lines.append("Metric reference: NOT_PRODUCED")
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
        lines.append("MEASURE DETAILS")

        for measure in score.measures:

            if not measure.metric_events:
                continue

            lines.append("")
            lines.append(
                f"Measure {measure.number}"
            )

            lines.append(
                "|1|2|3|4|"
            )

            for event in measure.metric_events:

                local_beat = (
                    event.beat_index % 4
                ) + 1

                lines.append(
                    f"  beat {local_beat}: "
                    f"{event.offset_ms:.1f} ms "
                    f"@ {event.absolute_time_seconds:.3f}s"
                )

        lines.append("")
        lines.append("=" * 70)
        lines.append("")

        lines.append("INSTRUMENTS")

        for lane in score.instrument_lanes:

            lines.append(f"{lane.name:<12}")

            for event in lane.metric_events:

                lines.append(
                    f"  beat {event.beat_index}: "
                    f"{event.offset_ms:.1f} ms "
                    f"@ {event.absolute_time_seconds:.3f}s"
                )

        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)
