from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from jga.domain.declared_metric_reference import MetricReferenceProvenance
from jga.domain.declared_metric_timeline import DeclaredAnalysisScope
from jga.interfaces.scientific_value_origin import ScientificValueOrigin


@dataclass(frozen=True, slots=True)
class BeatReference:
    """
    Represents one theoretical beat of the ensemble metric grid.

    A BeatReference is not directly observed.

    It is inferred from the recognised metric structure and
    acts as the temporal reference used to associate
    ElementaryMetricEvents to MetricClusters.
    """

    id: UUID

    index: int

    timestamp: float

    created_at: datetime

    supporting_pulse_candidate_ids: tuple[UUID, ...] = ()

    reconstruction_rule: str = "legacy-unrecorded"

    temporal_scope: str = "unspecified"

    exact_timestamp_seconds: Decimal | None = None

    exact_timestamp_ratio: str | None = None

    exact_period_seconds: Decimal | None = None

    exact_period_ratio: str | None = None

    epistemic_status: ScientificValueOrigin | None = None

    tempo_provenance: MetricReferenceProvenance | None = None

    phase_origin_provenance: MetricReferenceProvenance | None = None

    numeric_temporal_scope: DeclaredAnalysisScope | None = None

    def __post_init__(self):

        if self.index < 0:
            raise ValueError(
                "index must be non-negative"
            )

        if self.timestamp < 0.0:
            raise ValueError(
                "timestamp must be non-negative"
            )
