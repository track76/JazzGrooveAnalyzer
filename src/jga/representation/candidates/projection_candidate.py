"""
Projection Candidate

M15
"""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class ProjectionCandidate:
    """
    Fully validated Representation object ready
    for scientific projection.
    """

    representation_object: Any
