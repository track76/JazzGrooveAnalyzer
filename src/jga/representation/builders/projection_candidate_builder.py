"""
Projection Candidate Builder

M15
"""

from jga.representation.candidates import ProjectionCandidate


class ProjectionCandidateBuilder:
    """
    Builds ProjectionCandidate instances from validated
    Representation objects.

    This builder is the unique construction point of
    ProjectionCandidate inside the Representation Layer.
    """

    def build(self, representation_object):

        return ProjectionCandidate(
            representation_object=representation_object,
        )
