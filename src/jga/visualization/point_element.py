"""
Point Element.

Concrete graphic element representing
a point.
"""

from dataclasses import dataclass

from jga.visualization.graphic_element import (
    GraphicElement,
)


@dataclass(frozen=True, slots=True)
class PointElement(GraphicElement):
    """
    Point graphic element.

    Contains abstract geometric position.
    """

    position: tuple[float, float] = (0.0, 0.0)

    element_type: str = "point"
