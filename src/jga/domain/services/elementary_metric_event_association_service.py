from jga.domain.beat_reference import BeatReference
from jga.domain.elementary_metric_event_association import (
    ElementaryMetricEventAssociation,
)
from jga.domain.metric_contributor import MetricContributor
from jga.domain.pulse_candidate import PulseCandidate


class ElementaryMetricEventAssociationService:
    """Associate observations only through explicit BeatReference lineage."""

    RULE = "explicit-movement-observation-lineage/v1"

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
