"""
Visualization Annotation.

Represents an additional visual marker
attached to a visualization context.

It does not modify scientific data.
"""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class VisualizationAnnotation:
    """
    Immutable visual annotation.
    """

    timestamp: float
    label: str
    reference_id: UUID | None = None

    def __post_init__(self):

        if self.timestamp < 0:
            raise ValueError(
                "timestamp must be non-negative."
            )

        if not self.label:
            raise ValueError(
                "label must not be empty."
            )
