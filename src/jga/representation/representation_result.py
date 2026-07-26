"""
Representation Layer Result.

Collects all immutable scientific representations produced
by the Representation Layer.
"""

from dataclasses import dataclass

from jga.representation.metric_landscape import (
    MetricLandscape,
)


@dataclass(frozen=True, slots=True)
class RepresentationResult:
    """
    Output of the Representation Layer.
    """

    metric_landscape: MetricLandscape | None = None
