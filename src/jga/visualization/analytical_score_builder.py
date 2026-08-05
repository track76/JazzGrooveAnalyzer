"""
Analytical Score Builder.

Builds immutable AnalyticalScore objects.
"""

from jga.visualization.analytical_score import (
    AnalyticalScore,
)

from jga.runtime.analysis_context import (
    AnalysisContext,
)

from jga.visualization.measure import (
    Measure,
)

from jga.visualization.instrument_lane import (
    InstrumentLane,
)

from jga.visualization.metric_event import (
    MetricEvent,
)


class AnalyticalScoreBuilder:
    """
    Builds musicological analytical scores.

    M72.
    """

    def build(
        self,
        context: AnalysisContext,
    ) -> AnalyticalScore:

        measures_list = []

        representation_events = []

        if context.representation_result:

            landscape = (
                context.representation_result
                .metric_landscape
            )

            if landscape and landscape.metric_trajectory:

                representation_events = list(
                    landscape
                    .metric_trajectory
                    .metric_points
                )

        for measure in context.reconstructed_measures:

            metric_events = []

            for point in representation_events:

                event = point.event

                if (
                    measure.start_time_seconds
                    <= event.timestamp
                    <= measure.end_time_seconds
                ):

                    metric_events.append(
                        MetricEvent(
                            source_name="Unknown",
                            beat_index=point.beat_index,
                            absolute_time_seconds=event.timestamp,
                            offset_ms=point.offset_ms,
                        )
                    )

            measures_list.append(
                Measure(
                    number=measure.number,
                    time_signature=measure.time_signature,
                    bpm=measure.internal_bpm,
                    start_time_seconds=measure.start_time_seconds,
                    metric_events=tuple(metric_events),
                )
            )

        if representation_events:

            assigned = {
                event.absolute_time_seconds
                for measure in measures_list
                for event in measure.metric_events
            }

            last_measure = measures_list[-1]

            extra_events = []

            for point in representation_events:

                if point.event.timestamp not in assigned:

                    extra_events.append(
                        MetricEvent(
                            source_name="Unknown",
                            beat_index=point.beat_index,
                            absolute_time_seconds=(
                                point.event.timestamp
                            ),
                            offset_ms=point.offset_ms,
                        )
                    )

            if extra_events:

                measures_list[-1] = Measure(
                    number=last_measure.number,
                    time_signature=last_measure.time_signature,
                    bpm=last_measure.bpm,
                    start_time_seconds=last_measure.start_time_seconds,
                    metric_events=(
                        last_measure.metric_events
                        + tuple(extra_events)
                    ),
                )

        instrument_lanes = ()

        if context.representation_result:

            landscape = (
                context.representation_result
                .metric_landscape
            )

            if landscape and landscape.metric_trajectory:

                lanes = {}

                for point in (
                    landscape
                    .metric_trajectory
                    .metric_points
                ):

                    event = point.event

                    source_name = "Unknown"

                    if context.ensemble_analysis_result:

                        contributor_map = {
                            contributor.id: contributor.sound_source_id
                            for contributor
                            in context.ensemble_analysis_result.metric_contributors
                        }

                        source_map = {
                            source.id: source.name
                            for source
                            in context.ensemble_analysis_result.sound_sources
                        }

                        sound_source_id = contributor_map.get(
                            event.contributor_id
                        )

                        if sound_source_id is not None:

                            source_name = source_map.get(
                                sound_source_id,
                                "Unknown",
                            )

                    metric_event = MetricEvent(
                        source_name=source_name,
                        beat_index=point.beat_index,
                        absolute_time_seconds=(
                            event.timestamp
                        ),
                        offset_ms=(
                            point.offset_ms
                        ),
                    )

                    lanes.setdefault(
                        source_name,
                        [],
                    ).append(
                        metric_event
                    )

                instrument_lanes = tuple(
                    InstrumentLane(
                        name=name,
                        metric_events=tuple(events),
                    )
                    for name, events in lanes.items()
                )

        measures = tuple(measures_list)

        return AnalyticalScore(
            recording_title="",
            artist="",
            time_signature=(
                measures[0].time_signature
                if measures
                else "4/4"
            ),
            average_bpm=(
                measures[0].bpm
                if measures
                else 120.0
            ),
            sections=(),
            measures=measures,
            instrument_lanes=instrument_lanes,
        )
