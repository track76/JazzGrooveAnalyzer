"""
Projection Input

Scientific Geometric Projection

M14
"""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class ProjectionInput:
    """
    Immutable input of the Scientific Projection Engine.

    This object wraps a validated Representation object before
    scientific geometric projection.
    """

    representation_object: Any
