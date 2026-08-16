from datetime import datetime
from uuid import uuid4

from jga.domain.beat_reference import BeatReference
from jga.domain.elementary_metric_event import ElementaryMetricEvent
from jga.domain.elementary_metric_event_association import (
    ElementaryMetricEventAssociation,
)
from jga.domain.metric_cluster import MetricCluster
from jga.domain.services.beat_projection_engine import BeatProjectionEngine


class MetricClusterBuilder:
    """
    Builds MetricCluster objects by assigning
    already-materialized ElementaryMetricEvents to preceding BeatReferences.

    Every BeatReference produces a MetricCluster.
    Multiple events from one contributor may occupy the same cluster.
    """

    def __init__(self) -> None:
        self._projection_engine = BeatProjectionEngine()

    def build(
        self,
        beat_references: tuple[BeatReference, ...],
        events: tuple[ElementaryMetricEvent, ...],
        associations: tuple[ElementaryMetricEventAssociation, ...] = (),
    ) -> tuple[MetricCluster, ...]:

        if not beat_references:
            return ()

        ordered_beats = tuple(
            sorted(
                beat_references,
                key=lambda beat: (beat.timestamp, beat.index),
            )
        )
        beat_grid = tuple(beat.timestamp for beat in ordered_beats)
        beat_by_id = {beat.id: beat for beat in ordered_beats}
        assignments = {beat.id: [] for beat in ordered_beats}
        localization_by_event = {
            item.elementary_metric_event_id: item
            for item in associations
            if item.elementary_metric_event_id is not None
        }

        for event in events:
            localization = localization_by_event.get(event.id)
            if localization is not None:
                if localization.outcome != "ASSOCIATED":
                    raise ValueError("Every EME requires an authorized metric localization")
                try:
                    projected_beat = beat_by_id[localization.beat_reference_id]
                except KeyError as error:
                    raise ValueError(
                        "EME localization references a BeatReference outside the supplied timeline"
                    ) from error
            elif associations:
                raise ValueError("Every EME requires exactly one metric localization result")
            elif event.beat_reference_id is not None:
                try:
                    projected_beat = beat_by_id[event.beat_reference_id]
                except KeyError as error:
                    raise ValueError(
                        "EME references a BeatReference outside the supplied timeline"
                    ) from error
            else:
                # Compatibility for legacy EME that predate explicit
                # movement-association lineage.
                projected_timestamp = self._projection_engine.project(
                    event_timestamp=event.timestamp,
                    beat_grid=beat_grid,
                )
                projected_beat = next(
                    beat
                    for beat in ordered_beats
                    if beat.timestamp == projected_timestamp
                )
            assignments[projected_beat.id].append(event)

        return tuple(
            MetricCluster(
                id=uuid4(),
                beat_reference=beat,
                events=tuple(assignments[beat.id]),
                created_at=datetime.now(),
            )
            for beat in ordered_beats
        )
