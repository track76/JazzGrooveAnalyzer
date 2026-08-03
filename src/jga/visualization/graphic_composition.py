"""
Graphic Composition.

Domain entity representing a composition
of graphic elements.
"""

from dataclasses import dataclass, field

from jga.visualization.graphic_style import (
    GraphicStyle,
)


@dataclass(frozen=True, slots=True)
class GraphicComposition:
    """
    Abstract graphic composition entity.
    """

    elements: tuple = field(
        default_factory=tuple,
    )

    metadata: dict = field(
        default_factory=dict,
    )

    style: GraphicStyle | None = None

    def is_valid(
        self,
    ) -> bool:
        """
        Checks composition validity.
        """

        return True
