"""
Scientific Coordinate System.

Representation Layer container for scientific axes.
"""

from dataclasses import dataclass

from jga.representation.scientific_axis import (
    ScientificAxis,
)


@dataclass(frozen=True, slots=True)
class ScientificCoordinateSystem:
    """
    Immutable collection of scientific axes.

    The coordinate system defines scientific
    dimensions only.
    """

    axes: tuple[ScientificAxis, ...] = ()

    def get_axis(
        self,
        identifier: str,
    ) -> ScientificAxis | None:
        """
        Returns the scientific axis identified by
        its unique identifier.
        """

        for axis in self.axes:

            if axis.identifier == identifier:
                return axis

        return None
