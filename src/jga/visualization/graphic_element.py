"""
Graphic Element.

Base entity for visual graphic elements.
"""

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class GraphicElement:
    """
    Abstract graphic element.

    Concrete graphic elements extend
    this base entity.
    """

    element_type: str = "generic"

    metadata: dict = field(
        default_factory=dict,
    )

    def is_valid(
        self,
    ) -> bool:
        """
        Checks structural validity
        of the graphic element.
        """

        return bool(
            self.element_type
        )
