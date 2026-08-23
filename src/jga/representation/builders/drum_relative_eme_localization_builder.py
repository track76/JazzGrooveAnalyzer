"""Build neutral Drum-relative projections from authorized EME."""

from bisect import bisect_right
from collections.abc import Iterable
from decimal import Decimal, ROUND_HALF_UP

from jga.domain.elementary_metric_event import ElementaryMetricEvent
from jga.domain.pulse_candidate import PulseCandidate
from jga.representation.drum_relative_eme_localization import (
    DrumEMEReference,
    DrumRelativeEMELocalization,
    ObservationLineage,
)


class DrumRelativeEMELocalizationBuilder:
    RULE = "observed-drum-eme-relative-localization/v1"

    def build(
        self,
        target_events: Iterable[ElementaryMetricEvent],
        drum_events: Iterable[ElementaryMetricEvent],
        pulse_candidates: Iterable[PulseCandidate],
        *,
        temporal_origin_seconds: float,
        analysis_execution_id: str,
    ) -> tuple[DrumRelativeEMELocalization, ...]:
        candidates = {item.id: item for item in pulse_candidates}
        ordered_drums = tuple(
            sorted(drum_events, key=lambda item: (item.timestamp, str(item.id)))
        )
        drum_timestamps = tuple(item.timestamp for item in ordered_drums)
        results = []

        for target in sorted(
            target_events, key=lambda item: (item.timestamp, str(item.id))
        ):
            boundary = bisect_right(drum_timestamps, target.timestamp)
            preceding = ordered_drums[boundary - 1] if boundary else None
            following = ordered_drums[boundary] if boundary < len(ordered_drums) else None
            preceding_distance = (
                target.timestamp - preceding.timestamp if preceding is not None else None
            )
            following_distance = (
                target.timestamp - following.timestamp if following is not None else None
            )

            nearest, status = self._nearest(
                target.timestamp, ordered_drums, preceding, following
            )
            interval_fraction = None
            if (
                preceding is not None
                and following is not None
                and following.timestamp != preceding.timestamp
            ):
                interval_fraction = preceding_distance / (
                    following.timestamp - preceding.timestamp
                )

            results.append(
                DrumRelativeEMELocalization(
                    target_eme_id=target.id,
                    target_timestamp_seconds=target.timestamp,
                    target_contributor_id=target.contributor_id,
                    target_sound_source_id=self._required_source(target),
                    target_supporting_observations=self._lineage(target, candidates),
                    target_source_asset_sha256=target.source_asset_sha256,
                    target_temporal_scope=target.temporal_scope,
                    target_materialization_rule=target.materialization_rule,
                    preceding_drum_eme=self._reference(preceding, candidates),
                    following_drum_eme=self._reference(following, candidates),
                    distance_from_preceding_seconds=preceding_distance,
                    distance_from_following_seconds=following_distance,
                    nearest_drum_eme=self._reference(nearest, candidates),
                    nearest_displacement_seconds=(
                        target.timestamp - nearest.timestamp
                        if nearest is not None
                        else None
                    ),
                    nearest_selection_status=status,
                    observed_interval_fraction=interval_fraction,
                    temporal_origin_seconds=temporal_origin_seconds,
                    localization_rule=self.RULE,
                    analysis_execution_id=analysis_execution_id,
                )
            )
        return tuple(results)

    @staticmethod
    def format_absolute_time(timestamp_seconds: float) -> str:
        """Project numeric recording time to deterministic millisecond display."""
        total_ms = int(
            (Decimal(str(timestamp_seconds)) * 1000).quantize(
                Decimal("1"), rounding=ROUND_HALF_UP
            )
        )
        hours, remainder = divmod(total_ms, 3_600_000)
        minutes, remainder = divmod(remainder, 60_000)
        seconds, milliseconds = divmod(remainder, 1000)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"

    def _reference(self, event, candidates):
        if event is None:
            return None
        return DrumEMEReference(
            eme_id=event.id,
            contributor_id=event.contributor_id,
            sound_source_id=self._required_source(event),
            timestamp_seconds=event.timestamp,
            supporting_observations=self._lineage(event, candidates),
            source_asset_sha256=event.source_asset_sha256,
            temporal_scope=event.temporal_scope,
            materialization_rule=event.materialization_rule,
        )

    @staticmethod
    def _required_source(event: ElementaryMetricEvent):
        if event.sound_source_id is None:
            raise ValueError("Drum-relative localization requires sound_source_id")
        return event.sound_source_id

    @staticmethod
    def _lineage(event, candidates):
        lineage = []
        for candidate_id in event.supporting_pulse_candidate_ids:
            candidate = candidates.get(candidate_id)
            if candidate is None:
                raise ValueError(f"Missing PulseCandidate lineage: {candidate_id}")
            lineage.append(
                ObservationLineage(
                    pulse_candidate_id=candidate.id,
                    sound_source_id=candidate.sound_source_id,
                    observation_index=candidate.observation_index,
                    observation_provenance_id=candidate.observation_provenance_id,
                )
            )
        return tuple(lineage)

    @staticmethod
    def _nearest(target_timestamp, drums, preceding, following):
        if not drums:
            return None, "NOT_PRODUCED"
        minimum = min(abs(target_timestamp - item.timestamp) for item in drums)
        tied = tuple(
            item for item in drums if abs(target_timestamp - item.timestamp) == minimum
        )
        status = "EQUAL_DISTANCE_TIE" if len(tied) > 1 else "UNIQUE"
        if (
            preceding is not None
            and following is not None
            and abs(target_timestamp - preceding.timestamp)
            == abs(target_timestamp - following.timestamp)
            == minimum
        ):
            return preceding, status
        return min(tied, key=lambda item: str(item.id)), status
