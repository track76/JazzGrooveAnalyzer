"""
Line Element.

Concrete graphic element representing
a line.
"""

from dataclasses import dataclass, field

from jga.visualization.graphic_element import (
    GraphicElement,
)


@dataclass(frozen=True, slots=True)
class LineElement(GraphicElement):
    """
    Line graphic element.

    Contains abstract geometric points.
    """

    points: tuple[tuple[float, float], ...] = field(
        default_factory=tuple,
    )

    element_type: str = "line"
