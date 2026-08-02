
from dataclasses import dataclass

from jga.domain.beat_reference import BeatReference
from jga.domain.elementary_metric_event import (
    ElementaryMetricEvent,
)
from jga.domain.internal_metric_timeline import (
    InternalMetricTimeline,
)
from jga.domain.metric_cluster import MetricCluster
from jga.domain.pulse import Pulse


@dataclass(frozen=True, slots=True)
class DomainReconstructionResult:
    """
    Explicit output contract for domain metric reconstruction.

    Contains only reconstructed domain objects.

    It must not depend on runtime context
    or acquisition layers.
    """

    domain_pulse_candidates: tuple

    elementary_metric_events: (
        tuple[ElementaryMetricEvent, ...]
    )

    beat_references: (
        tuple[BeatReference, ...]
    )

    metric_clusters: (
        tuple[MetricCluster, ...]
    )

    pulses: (
        tuple[Pulse, ...]
    )

    internal_metric_timeline: (
        InternalMetricTimeline
    )
