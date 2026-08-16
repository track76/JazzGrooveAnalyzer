"""Reconstruct movement anchors from authorized pre-EME metric evidence."""

from datetime import datetime, timezone
from decimal import Decimal
from fractions import Fraction
from math import ceil
from uuid import NAMESPACE_URL, uuid5

from jga.core.ensemble_metric_event import EnsembleMetricEvent
from jga.domain.beat_reference import BeatReference
from jga.domain.declared_metric_reference import DeclaredMetricReference
from jga.domain.declared_metric_timeline import (
    DeclaredAnalysisScope,
    DeclaredQuarterPhaseOrigin,
)
from jga.interfaces.scientific_value_origin import ScientificValueOrigin


class BeatReconstructionEngine:
    """Construct BeatReferences without depending on EME input."""

    OBSERVED_RULE = "ensemble-consensus-anchor/v1"
    DECLARED_PERIOD_RULE = "declared-quarter-origin-index-scope/v1"

    def reconstruct(
        self,
        ensemble_metric_events: tuple[EnsembleMetricEvent, ...],
        declared_metric_reference: DeclaredMetricReference | None = None,
        declared_quarter_phase_origin: DeclaredQuarterPhaseOrigin | None = None,
        declared_analysis_scope: DeclaredAnalysisScope | None = None,
    ) -> tuple[BeatReference, ...]:
        ordered = tuple(
            sorted(
                ensemble_metric_events,
                key=lambda event: (event.beat_time, event.start_time, event.end_time),
            )
        )
        if declared_metric_reference is not None:
            if declared_quarter_phase_origin is None or declared_analysis_scope is None:
                raise ValueError(
                    "declared metric reference requires declared phase origin and numeric scope"
                )
            return self._reconstruct_declared(
                ordered,
                declared_metric_reference,
                declared_quarter_phase_origin,
                declared_analysis_scope,
            )

        if not ordered:
            return ()

        beats = []
        for index, event in enumerate(ordered):
            observation_ids = tuple(
                contribution.pulse_candidate_id
                for contribution in event.contributions
                if contribution.pulse_candidate_id is not None
            )
            identity = ",".join(str(item) for item in observation_ids)
            timestamp = (
                event.beat_time
            )
            beats.append(
                BeatReference(
                    id=uuid5(
                        NAMESPACE_URL,
                        f"{self.OBSERVED_RULE}:{index}:{timestamp:.17g}:{identity}",
                    ),
                    index=index,
                    timestamp=timestamp,
                    created_at=datetime.now(),
                    supporting_pulse_candidate_ids=observation_ids,
                    reconstruction_rule=self.OBSERVED_RULE,
                    temporal_scope="analysis_input",
                )
            )
        return tuple(beats)

    def _reconstruct_declared(
        self,
        ordered: tuple[EnsembleMetricEvent, ...],
        reference: DeclaredMetricReference,
        phase: DeclaredQuarterPhaseOrigin,
        scope: DeclaredAnalysisScope,
    ) -> tuple[BeatReference, ...]:
        if reference.beat_unit != "quarter":
            raise ValueError("quarter BeatReference reconstruction requires beat_unit=quarter")
        if phase.provenance.source_sha256 != scope.asset_sha256:
            raise ValueError("phase origin must be bound to the declared scope asset")
        period = Fraction(60, 1) / Fraction(reference.beats_per_minute)
        origin = Fraction(phase.seconds)
        scope_start = Fraction(scope.start_seconds)
        scope_end = Fraction(scope.end_seconds)
        if origin >= scope_end:
            raise ValueError("declared phase origin must precede declared scope end")

        exact_timestamps = []
        index = max(0, ceil((scope_start - origin) / period))
        while True:
            timestamp = origin + index * period
            if timestamp >= scope_end:
                break
            exact_timestamps.append(timestamp)
            index += 1

        support_by_index: dict[int, list] = {
            index: [] for index in range(len(exact_timestamps))
        }
        float_timestamps = tuple(float(item) for item in exact_timestamps)
        for event in ordered:
            nearest_index = min(
                range(len(float_timestamps)),
                key=lambda item: (abs(event.beat_time - float_timestamps[item]), item),
            )
            support_by_index[nearest_index].extend(
                contribution.pulse_candidate_id
                for contribution in event.contributions
                if contribution.pulse_candidate_id is not None
            )

        identity_context = ":".join(
            (
                self.DECLARED_PERIOD_RULE,
                str(reference.beats_per_minute),
                reference.beat_unit,
                reference.provenance.source_id,
                reference.provenance.source_sha256,
                phase.provenance.source_id,
                phase.provenance.source_sha256,
                scope.asset_sha256,
                str(scope_start),
                str(scope_end),
            )
        )
        created_at = datetime.now(timezone.utc)
        return tuple(
            BeatReference(
                id=uuid5(
                    NAMESPACE_URL,
                    f"{identity_context}:{index}:{timestamp}",
                ),
                index=index,
                timestamp=float(timestamp),
                exact_timestamp_seconds=(
                    Decimal(timestamp.numerator) / Decimal(timestamp.denominator)
                ),
                exact_timestamp_ratio=(
                    f"{timestamp.numerator}/{timestamp.denominator}"
                ),
                exact_period_seconds=(
                    Decimal(period.numerator) / Decimal(period.denominator)
                ),
                exact_period_ratio=f"{period.numerator}/{period.denominator}",
                created_at=created_at,
                supporting_pulse_candidate_ids=tuple(support_by_index[index]),
                reconstruction_rule=self.DECLARED_PERIOD_RULE,
                temporal_scope=(
                    f"[{scope.start_seconds},{scope.end_seconds})"
                ),
                epistemic_status=ScientificValueOrigin.DECLARED,
                tempo_provenance=reference.provenance,
                phase_origin_provenance=phase.provenance,
                numeric_temporal_scope=scope,
            )
            for index, timestamp in enumerate(exact_timestamps)
        )
