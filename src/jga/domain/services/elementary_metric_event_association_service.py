from bisect import bisect_right

from jga.domain.beat_reference import BeatReference
from jga.domain.elementary_metric_event import ElementaryMetricEvent
from jga.domain.elementary_metric_event_association import (
    ElementaryMetricEventAssociation,
)
from jga.domain.metric_contributor import MetricContributor
from jga.domain.pulse_candidate import PulseCandidate


class ElementaryMetricEventAssociationService:
    """Localize existing EME without controlling their existence."""

    RULE = "explicit-movement-observation-lineage/v1"
    LOCALIZATION_RULE = "preceding-quarter-localization/v1"

    def localize(
        self,
        events: tuple[ElementaryMetricEvent, ...],
        beat_references: tuple[BeatReference, ...],
    ) -> tuple[ElementaryMetricEventAssociation, ...]:
        ordered_beats = tuple(
            sorted(beat_references, key=lambda beat: (beat.timestamp, beat.index))
        )
        timestamps = tuple(beat.timestamp for beat in ordered_beats)
        results = []
        for event in events:
            declared_quarter_timeline = bool(
                ordered_beats and ordered_beats[0].exact_period_seconds is not None
            )
            if ordered_beats and not declared_quarter_timeline:
                nearest = min(
                    ordered_beats,
                    key=lambda beat: (abs(event.timestamp - beat.timestamp), beat.index),
                )
                results.append(
                    ElementaryMetricEventAssociation(
                        beat_reference_id=nearest.id,
                        contributor_id=event.contributor_id,
                        sound_source_id=event.sound_source_id,
                        supporting_pulse_candidate_ids=event.supporting_pulse_candidate_ids,
                        timestamp=event.timestamp,
                        confidence=event.confidence,
                        temporal_scope=event.temporal_scope,
                        association_rule="legacy-nearest-localization/v1",
                        outcome="ASSOCIATED",
                        elementary_metric_event_id=event.id,
                        elapsed_seconds=event.timestamp - nearest.timestamp,
                    )
                )
                continue
            preceding_index = bisect_right(timestamps, event.timestamp) - 1
            if preceding_index < 0 or not ordered_beats:
                results.append(
                    ElementaryMetricEventAssociation(
                        beat_reference_id=None,
                        contributor_id=event.contributor_id,
                        sound_source_id=event.sound_source_id,
                        supporting_pulse_candidate_ids=(
                            event.supporting_pulse_candidate_ids
                        ),
                        timestamp=event.timestamp,
                        confidence=event.confidence,
                        temporal_scope=event.temporal_scope,
                        association_rule=self.LOCALIZATION_RULE,
                        outcome="NOT_PRODUCED",
                        elementary_metric_event_id=event.id,
                    )
                )
                continue

            preceding = ordered_beats[preceding_index]
            following = (
                ordered_beats[preceding_index + 1]
                if preceding_index + 1 < len(ordered_beats)
                else None
            )
            if preceding.exact_period_seconds is None:
                period_seconds = (
                    following.timestamp - preceding.timestamp
                    if following is not None
                    else None
                )
            else:
                period_seconds = float(preceding.exact_period_seconds)
            elapsed = event.timestamp - preceding.timestamp
            phase = (
                elapsed / period_seconds
                if period_seconds is not None and period_seconds > 0
                else None
            )
            outcome = (
                "ASSOCIATED"
                if phase is not None and 0.0 <= phase < 1.0
                else "NOT_PRODUCED"
            )
            results.append(
                ElementaryMetricEventAssociation(
                    beat_reference_id=(preceding.id if outcome == "ASSOCIATED" else None),
                    contributor_id=event.contributor_id,
                    sound_source_id=event.sound_source_id,
                    supporting_pulse_candidate_ids=event.supporting_pulse_candidate_ids,
                    timestamp=event.timestamp,
                    confidence=event.confidence,
                    temporal_scope=event.temporal_scope,
                    association_rule=self.LOCALIZATION_RULE,
                    outcome=outcome,
                    elementary_metric_event_id=event.id,
                    following_beat_reference_id=(
                        following.id if following is not None else None
                    ),
                    elapsed_seconds=elapsed if outcome == "ASSOCIATED" else None,
                    normalized_phase=phase if outcome == "ASSOCIATED" else None,
                )
            )
        return tuple(results)

    def associate(
        self,
        pulse_candidates: tuple[PulseCandidate, ...],
        contributors: tuple[MetricContributor, ...],
        beat_references: tuple[BeatReference, ...],
    ) -> tuple[ElementaryMetricEventAssociation, ...]:
        candidates = {candidate.id: candidate for candidate in pulse_candidates}
        contributor_by_source = {
            contributor.sound_source_id: contributor for contributor in contributors
        }
        movement_membership_counts: dict = {}
        for beat in beat_references:
            for candidate_id in beat.supporting_pulse_candidate_ids:
                movement_membership_counts[candidate_id] = (
                    movement_membership_counts.get(candidate_id, 0) + 1
                )
        multiply_assigned_ids = {
            candidate_id
            for candidate_id, count in movement_membership_counts.items()
            if count > 1
        }
        results = []

        for beat in beat_references:
            movement_candidates = tuple(
                candidates[candidate_id]
                for candidate_id in beat.supporting_pulse_candidate_ids
                if candidate_id in candidates
            )
            by_source: dict = {}
            for candidate in movement_candidates:
                by_source.setdefault(candidate.sound_source_id, []).append(candidate)

            for sound_source_id, observations in sorted(
                by_source.items(), key=lambda item: str(item[0])
            ):
                contributor = contributor_by_source.get(sound_source_id)
                if contributor is None:
                    continue
                ordered = tuple(sorted(observations, key=lambda item: (item.timestamp, str(item.id))))
                timestamps = {item.timestamp for item in ordered}
                associated = (
                    len(timestamps) == 1
                    and not any(item.id in multiply_assigned_ids for item in ordered)
                )
                results.append(
                    ElementaryMetricEventAssociation(
                        beat_reference_id=beat.id,
                        contributor_id=contributor.id,
                        sound_source_id=sound_source_id,
                        supporting_pulse_candidate_ids=tuple(item.id for item in ordered),
                        timestamp=ordered[0].timestamp if associated else None,
                        confidence=min(item.confidence for item in ordered) if associated else None,
                        temporal_scope=beat.temporal_scope,
                        association_rule=self.RULE,
                        outcome="ASSOCIATED" if associated else "AMBIGUOUS",
                    )
                )

        return tuple(results)
