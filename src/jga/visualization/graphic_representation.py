"""
Graphic Representation.

Represents the abstract structure
of visual graphic elements.
"""

from dataclasses import dataclass, field

from jga.visualization.materialized_plot import (
    MaterializedPlot,
)


@dataclass(frozen=True, slots=True)
class GraphicRepresentation:
    """
    Abstract graphic representation.

    Keeps traceability to the source
    materialized plot and metadata.
    """

    source_plot: MaterializedPlot | None = None

    metadata: dict = field(
        default_factory=dict,
    )

    def is_valid(
        self,
    ) -> bool:
        """
        Checks structural validity
        of the graphic representation.
        """

        return (
            self.source_plot is not None
            and self.metadata is not None
        )
