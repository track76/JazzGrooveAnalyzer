"""
Visual Point.

Visualization Layer graphical coordinate.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class VisualPoint:
    """
    Immutable graphical point.

    Visual coordinates belong exclusively
    to the Visualization Layer.
    """

    x: float

    y: float
