from dataclasses import dataclass

from jga.domain.beat_reference import BeatReference
from jga.domain.metric_cluster import MetricCluster
from jga.domain.declared_metric_reference import DeclaredMetricReference


@dataclass(
    frozen=True,
    slots=True,
)
class ReconstructedMeasure:
    """
    One reconstructed musical measure.
    """

    number: int

    time_signature: str

    internal_bpm: float

    start_time_seconds: float

    end_time_seconds: float

    beat_references: tuple[
        BeatReference,
        ...
    ]

    metric_clusters: tuple[
        MetricCluster,
        ...
    ]

    declared_metric_reference: DeclaredMetricReference | None = None
