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

    The temporal position identifies where
    the represented point belongs within
    the analyzed recording.

    No scientific interpretation is attached
    to this value.
    """

    x: float

    y: float

    time: float

    def __post_init__(self) -> None:
        if self.time < 0:
            raise ValueError("time must be non-negative.")
