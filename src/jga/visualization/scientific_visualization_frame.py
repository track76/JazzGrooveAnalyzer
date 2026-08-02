"""
Scientific Visualization Frame.

Visualization Layer container.

Consumes scientific representations without
modifying their meaning.
"""

from dataclasses import dataclass

from jga.representation.metric_landscape import (
    MetricLandscape,
)


@dataclass(frozen=True, slots=True)
class ScientificVisualizationFrame:
    """
    Immutable visualization input frame.

    The Visualization Layer consumes
    Representation objects only.
    """

    metric_landscape: MetricLandscape
