"""
Representation Layer Result.

Collects all immutable scientific representations produced
by the Representation Layer.
"""

from dataclasses import dataclass

from jga.representation.metric_cluster_portrait import (
    MetricClusterPortrait,
)


@dataclass(frozen=True, slots=True)
class RepresentationResult:
    """
    Output of the Representation Layer.
    """

    metric_cluster_portraits: tuple[
        MetricClusterPortrait,
        ...
    ] = ()
