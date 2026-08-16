from dataclasses import dataclass

from jga.core.metric_context import MetricContext
from jga.core.ensemble_metric_event import EnsembleMetricEvent
from jga.domain.metric_contributor import MetricContributor
from jga.domain.sound_source import SoundSource
from jga.domain.declared_metric_reference import DeclaredMetricReference
from jga.domain.declared_metric_timeline import (
    DeclaredAnalysisScope,
    DeclaredQuarterPhaseOrigin,
)
from jga.domain.declared_meter import DeclaredMeter


@dataclass(frozen=True, slots=True)
class DomainReconstructionInput:
    """
    Explicit input contract for domain metric reconstruction.

    Contains only semantic and metric information.
    It must not depend on audio acquisition
    or source observation layers.
    """

    sound_sources: tuple[SoundSource, ...]

    metric_context: MetricContext

    metric_contributors: tuple[MetricContributor, ...]

    domain_pulse_candidates: tuple

    ensemble_metric_events: tuple[EnsembleMetricEvent, ...]

    declared_metric_reference: DeclaredMetricReference | None = None

    declared_quarter_phase_origin: DeclaredQuarterPhaseOrigin | None = None

    declared_analysis_scope: DeclaredAnalysisScope | None = None

    declared_meter: DeclaredMeter | None = None
