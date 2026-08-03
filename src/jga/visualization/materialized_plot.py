"""
Materialized Plot.

Represents a concrete in-memory
plot structure.
"""

from dataclasses import dataclass, field

from jga.visualization.plot_representation import (
    PlotRepresentation,
)


@dataclass(frozen=True, slots=True)
class MaterializedPlot:
    """
    Materialized scientific plot.

    Keeps traceability to the source
    plot representation and metadata.
    """

    source_representation: PlotRepresentation | None = None

    metadata: dict = field(
        default_factory=dict,
    )

    def is_valid(
        self,
    ) -> bool:
        """
        Checks structural validity
        of the materialized plot.
        """

        return (
            self.source_representation is not None
            and self.metadata is not None
        )
