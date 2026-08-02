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

        NOTE:
        This engine currently has no access to
        temporal information.

        The canonical temporal propagation is
        performed by the
        MetricLandscapeVisualizationAdapter.

        TODO (Future Architecture Decision):
        Move VisualPoint creation exclusively
        into the canonical visualization
        adapter and let this engine return a
        pure ScientificProjection.
        """

        return VisualPoint(
            x=projection.visual_value,
            y=projection.visual_value,
            time=0.0,
        )
