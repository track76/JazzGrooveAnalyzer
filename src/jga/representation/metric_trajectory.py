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
    """

    metric_points: tuple = ()
