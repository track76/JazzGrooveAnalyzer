"""
Graphic Representation.

Represents the abstract structure
of visual graphic elements.
"""

from dataclasses import dataclass, field

from jga.visualization.materialized_plot import (
    MaterializedPlot,
)

from jga.visualization.graphic_element import (
    GraphicElement,
)


@dataclass(frozen=True, slots=True)
class GraphicRepresentation:
    """
    Abstract graphic representation.

    Keeps traceability to the source
    plot and contains graphic elements.
    """

    source_plot: MaterializedPlot | None = None

    metadata: dict = field(
        default_factory=dict,
    )

    elements: tuple[GraphicElement, ...] = field(
        default_factory=tuple,
    )

    def is_valid(
        self,
    ) -> bool:
        """
        Checks structural validity.
        """

        return (
            self.source_plot is not None
            and self.metadata is not None
        )
