"""
Scientific Projection Engine

M15
"""

from jga.representation.candidates import ProjectionCandidate


class ScientificProjectionEngine:
    """
    Identity implementation of the scientific projection.

    Numerical geometry will be introduced in later milestones.
    """

    def project(
        self,
        candidate: ProjectionCandidate,
    ) -> ProjectionCandidate:
        return candidate
