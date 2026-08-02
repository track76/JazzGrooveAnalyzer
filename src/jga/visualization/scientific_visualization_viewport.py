"""
Scientific Visualization Viewport.

Defines the observable region of a
ScientificVisualizationScene.

The viewport belongs exclusively to the
Visualization Layer.

It does not modify scientific meaning.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ScientificVisualizationViewport:
    """
    Immutable visualization viewport.

    Defines the visible region of a
    ScientificVisualizationScene.
    """

    x_min: float
    x_max: float

    y_min: float
    y_max: float

    def __post_init__(self) -> None:

        if self.x_max < self.x_min:
            raise ValueError(
                "x_max must be greater than or equal to x_min"
            )

        if self.y_max < self.y_min:
            raise ValueError(
                "y_max must be greater than or equal to y_min"
            )
