"""
Rendered Output.

Domain entity representing renderer output.
"""

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class RenderedOutput:
    """
    Abstract rendered output entity.
    """

    metadata: dict = field(
        default_factory=dict,
    )

    content: object | None = None
