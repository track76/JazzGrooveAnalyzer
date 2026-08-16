from datetime import datetime
from uuid import NAMESPACE_URL, uuid5

from jga.domain.elementary_metric_event import ElementaryMetricEvent
from jga.domain.elementary_metric_event_association import (
    ElementaryMetricEventAssociation,
)


class ElementaryMetricEventBuilder:
    """Materialize EME only from authorized association results."""

    def build(
        self,
        associations: tuple[ElementaryMetricEventAssociation, ...],
    ) -> tuple[ElementaryMetricEvent, ...]:
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
