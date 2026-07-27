"""
Scientific Projection Engine

M14
"""

from jga.representation.metric_point import MetricPoint


class ScientificProjectionEngine:
    """
    First executable implementation of the
    Scientific Geometric Projection.

    Numerical geometry is intentionally deferred.
    """

    def project(self, representation_object: MetricPoint) -> MetricPoint:
        """
        Identity projection.

        Until the scientific coordinate equations are formally
        introduced, projection preserves the Representation object
        unchanged.
        """
        return representation_object
