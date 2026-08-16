"""Reconstruct movement anchors from authorized pre-EME metric evidence."""

from datetime import datetime
from uuid import NAMESPACE_URL, uuid5

from jga.core.ensemble_metric_event import EnsembleMetricEvent
from jga.domain.beat_reference import BeatReference
from jga.domain.declared_metric_reference import DeclaredMetricReference


class BeatReconstructionEngine:
    """Construct BeatReferences without depending on EME input."""

    OBSERVED_RULE = "ensemble-consensus-anchor/v1"
    DECLARED_PERIOD_RULE = "ensemble-consensus-declared-period/v1"

    def reconstruct(
        self,
        ensemble_metric_events: tuple[EnsembleMetricEvent, ...],
        declared_metric_reference: DeclaredMetricReference | None = None,
    ) -> tuple[BeatReference, ...]:
        ordered = tuple(
            sorted(
                ensemble_metric_events,
                key=lambda event: (event.beat_time, event.start_time, event.end_time),
            )
        )
        if not ordered:
            return ()

        if declared_metric_reference is not None:
            period = float(declared_metric_reference.period_seconds)
            rule = self.DECLARED_PERIOD_RULE
        else:
            period = None
            rule = self.OBSERVED_RULE

        origin = ordered[0].beat_time
        beats = []
        for index, event in enumerate(ordered):
            observation_ids = tuple(
                contribution.pulse_candidate_id
                for contribution in event.contributions
                if contribution.pulse_candidate_id is not None
            )
            identity = ",".join(str(item) for item in observation_ids)
            timestamp = (
                origin + index * period
                if period is not None
                else event.beat_time
            )
            beats.append(
                BeatReference(
                    id=uuid5(
                        NAMESPACE_URL,
                        f"{rule}:{index}:{timestamp:.17g}:{identity}",
                    ),
                    index=index,
                    timestamp=timestamp,
                    created_at=datetime.now(),
                    supporting_pulse_candidate_ids=observation_ids,
                    reconstruction_rule=rule,
                    temporal_scope="analysis_input",
                )
            )
        return tuple(beats)
