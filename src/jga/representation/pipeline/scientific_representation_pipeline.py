"""
Scientific Representation Pipeline

M15
"""

from jga.representation.candidates import ProjectionCandidate
from jga.representation.projection import ScientificProjectionEngine


class ScientificRepresentationPipeline:

    def __init__(self):

        self._projection = ScientificProjectionEngine()

    def run(self, event, offset_ms):

        candidate = ProjectionCandidate(
            event=event,
            offset_ms=offset_ms,
        )

        return self._projection.project(candidate)
