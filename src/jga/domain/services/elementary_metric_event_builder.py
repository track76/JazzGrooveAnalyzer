from datetime import datetime
from uuid import NAMESPACE_URL, uuid5

from jga.domain.elementary_metric_event import ElementaryMetricEvent
from jga.domain.elementary_metric_event_association import (
    ElementaryMetricEventAssociation,
)
from jga.domain.metric_contributor import MetricContributor
from jga.domain.pulse_candidate import PulseCandidate


class ElementaryMetricEventBuilder:
    """Materialize source-event EME independently of metric localization."""

    RULE = "source-observation-event/v1"

    def build_from_observations(
        self,
        pulse_candidates: tuple[PulseCandidate, ...],
        contributors: tuple[MetricContributor, ...],
        temporal_scope: str,
        source_asset_sha256: str | None,
    ) -> tuple[ElementaryMetricEvent, ...]:
        contributor_by_source = {
            contributor.sound_source_id: contributor for contributor in contributors
        }
        events = []
        for candidate in sorted(
            pulse_candidates,
            key=lambda item: (
                item.timestamp,
                item.observation_index if item.observation_index is not None else -1,
                str(item.id),
            ),
        ):
            contributor = contributor_by_source.get(candidate.sound_source_id)
            if contributor is None:
                continue
            identity = ":".join(
                (
                    self.RULE,
                    source_asset_sha256 or "unbound-asset",
                    str(candidate.id),
                )
            )
            events.append(
                ElementaryMetricEvent(
                    id=uuid5(NAMESPACE_URL, identity),
                    contributor_id=contributor.id,
                    timestamp=candidate.timestamp,
                    confidence=candidate.confidence,
                    created_at=datetime.now(),
                    sound_source_id=candidate.sound_source_id,
                    supporting_pulse_candidate_ids=(candidate.id,),
                    association_rule="metric-localization-separate/ad-037",
                    temporal_scope=temporal_scope,
                    association_outcome="NOT_APPLICABLE",
                    evidence_status="OBSERVATION_SUPPORTED",
                    materialization_rule=self.RULE,
                    source_asset_sha256=source_asset_sha256,
                )
            )
        return tuple(events)

    def build(
        self,
        associations: tuple[ElementaryMetricEventAssociation, ...],
    ) -> tuple[ElementaryMetricEvent, ...]:
        """Legacy movement-dependent materialization retained for replay."""
        events = []
        for association in associations:
            if association.outcome != "ASSOCIATED":
                continue
            if association.timestamp is None or association.confidence is None:
                continue
            identity = ",".join(
                str(item) for item in association.supporting_pulse_candidate_ids
            )
            events.append(
                ElementaryMetricEvent(
                    id=uuid5(
                        NAMESPACE_URL,
                        f"{association.association_rule}:{association.beat_reference_id}:{association.contributor_id}:{identity}",
                    ),
                    contributor_id=association.contributor_id,
                    timestamp=association.timestamp,
                    confidence=association.confidence,
                    created_at=datetime.now(),
                    beat_reference_id=association.beat_reference_id,
                    sound_source_id=association.sound_source_id,
                    supporting_pulse_candidate_ids=(
                        association.supporting_pulse_candidate_ids
                    ),
                    association_rule=association.association_rule,
                    temporal_scope=association.temporal_scope,
                    association_outcome=association.outcome,
                    evidence_status="OBSERVATION_SUPPORTED",
                )
            )
        return tuple(events)
