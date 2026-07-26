"""
Metric Landscape.

Scientific representation of the complete
metric behaviour of one musical performance.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MetricLandscape:
    """
    Collection of Metric Cluster Portraits
    representing one complete performance.
    """

    metric_cluster_portraits: tuple = ()
