from jga.visualization.analytical_groove_point import (
    AnalyticalGroovePoint,
)


class AnalyticalGrooveBuilder:
    """
    Converts AnalyticalScore into visualization points.
    """

    def build(self, score):

        points = []

        for measure in score.measures:

            for event in measure.metric_events:

                points.append(
                    AnalyticalGroovePoint(
                        measure_number=measure.number,
                        instrument=event.source_name,
                        theoretical_beat=event.beat_index,
                        absolute_time_seconds=(
                            event.absolute_time_seconds
                        ),
                        bpm=measure.bpm,
                        offset_ms=event.offset_ms,
                    )
                )

        return tuple(points)
