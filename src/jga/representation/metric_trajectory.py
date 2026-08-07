"""
Metric Trajectory.

Temporal geometric path through one
Metric Landscape.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MetricTrajectory:
    """
    Ordered geometric trajectory of one
    musical performance.

    The trajectory preserves both:

    - reconstructed metric movements
    - observed Elementary Metric Events
    """

    metric_points: tuple = ()

    metric_cluster_portraits: tuple = ()
