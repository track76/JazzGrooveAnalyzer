"""
Metric Cluster Portrait.

Scientific references:

- G-004 Metric Cluster Portrait Geometry
- A-004 Representation Model
- A-005 Representation Contracts
"""

from dataclasses import dataclass

from jga.domain.metric_cluster import MetricCluster

from jga.representation.metric_point import MetricPoint


@dataclass(frozen=True, slots=True)
class MetricClusterPortrait:
    """
    Immutable geometric representation of one Metric Cluster.
    """

    metric_cluster: MetricCluster

    points: tuple[MetricPoint, ...]
