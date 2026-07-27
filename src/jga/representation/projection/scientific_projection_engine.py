"""
Scientific Projection Engine

M14
"""

from jga.representation.projection.projection_input import ProjectionInput


class ScientificProjectionEngine:
    """
    Identity implementation of the scientific projection.

    Geometry will be introduced in later milestones.
    """

    def project(
        self,
        projection_input: ProjectionInput,
    ) -> ProjectionInput:
        return projection_input
