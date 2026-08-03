"""
Graphic Style.

Domain entity describing visual
properties of graphic elements.
"""

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class GraphicStyle:
    """
    Abstract graphic style entity.
    """

    style_type: str = "default"

    metadata: dict = field(
        default_factory=dict,
    )

    def is_valid(
        self,
    ) -> bool:
        """
        Checks style validity.
        """

        return bool(
            self.style_type
        )
