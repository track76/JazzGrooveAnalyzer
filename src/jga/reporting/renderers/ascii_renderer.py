from jga.reporting.analytical_score import (
    AnalyticalScore,
)


class AnalyticalScoreAsciiRenderer:
    """
    Renders an AnalyticalScore as plain text.
    """

    def render(
        self,
        score: AnalyticalScore,
    ) -> str:

        lines: list[str] = []

        lines.append("=" * 72)
        lines.append("JAZZ GROOVE ANALYZER")
        lines.append("ANALYTICAL SCORE")
        lines.append("=" * 72)
        lines.append("")
        lines.append(f"Title  : {score.title}")
        lines.append(f"Artist : {score.artist}")
        lines.append("")

        for bar in score.bars:

            lines.append("-" * 72)

            lines.append(
                f"BAR {bar.number}"
            )

            lines.append(
                f"Time {bar.time_seconds:.2f}s"
            )

            lines.append(
                f"Meter {bar.time_signature}"
            )

            lines.append(
                f"Internal BPM {bar.internal_bpm:.2f}"
            )

            lines.append("-" * 72)

            for beat in bar.beats:

                lines.append(
                    f" Beat {beat.number}"
                )

                for cell in beat.cells:

                    flag = " ▲" if cell.significant_change else ""

                    lines.append(
                        f"   {cell.instrument:<15}"
                        f"{cell.offset_ms:+7.2f} ms"
                        f"{flag}"
                    )

            lines.append("")

        return "\n".join(lines)

