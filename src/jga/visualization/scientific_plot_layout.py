"""
Scientific Plot Layout.

Defines the structural organization
of a scientific visualization.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ScientificPlotLayout:
    """
    Scientific plot layout definition.
    """

    title: str

    x_axis: str

    y_axis: str

    def is_valid(
        self,
    ) -> bool:
        """
        Checks layout validity.
        """

        return bool(
            self.title
            and self.x_axis
            and self.y_axis
        )
