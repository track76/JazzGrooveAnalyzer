"""
Graphic Scene.

Domain entity representing a visual scene.
"""

from dataclasses import dataclass, field

from jga.visualization.graphic_style import (
    GraphicStyle,
)


@dataclass(frozen=True, slots=True)
class GraphicScene:
    """
    Abstract graphic scene entity.
    """

    compositions: tuple = field(
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
        Checks scene validity.
        """

        return True
