"""
Visualization Projection Context.

Carries visualization exploration parameters
through the Visualization Layer.

This object belongs exclusively to the
Visualization Layer.

It never contains scientific data.
"""

from dataclasses import dataclass

from jga.visualization.scientific_visualization_viewport import (
    ScientificVisualizationViewport,
)
from jga.visualization.temporal_visualization_window import (
    TemporalVisualizationWindow,
)


@dataclass(frozen=True, slots=True)
class VisualizationProjectionContext:
    """
    Immutable visualization projection context.

    Collects visualization exploration
    parameters required by visualization
    projectors.
    """

    temporal_window: (
        TemporalVisualizationWindow | None
    ) = None

    viewport: (
        ScientificVisualizationViewport | None
    ) = None
