"""
Scientific Projection Engine.

Visualization Layer projection service.
"""

from jga.visualization.scientific_projection import (
    ScientificProjection,
)

from jga.visualization.visual_point import (
    VisualPoint,
)


class ScientificProjectionEngine:
    """
    Projects scientific coordinates into
    visualization coordinates.
    """

    def project(
        self,
        projection: ScientificProjection,
    ) -> VisualPoint:
        """
        Deterministic projection.

        Current implementation preserves
        the visual value directly.
        """

        return VisualPoint(
            x=projection.visual_value,
            y=projection.visual_value,
        )
