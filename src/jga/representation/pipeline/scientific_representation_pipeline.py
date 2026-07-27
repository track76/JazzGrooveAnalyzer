"""
Scientific Representation Pipeline

M15
"""

from jga.representation.candidates import ProjectionCandidate
from jga.representation.projection import (
    ProjectionInput,
    ScientificProjectionEngine,
)


class ScientificRepresentationPipeline:

    def __init__(self):

        self._projection = ScientificProjectionEngine()

    def run(self, representation_object):

        candidate = ProjectionCandidate(
            representation_object=representation_object,
        )

        projection_input = ProjectionInput(
            representation_object=candidate,
        )

        return self._projection.project(
            projection_input,
        )
