from dataclasses import dataclass

from jga.reporting.analytical_cell import (
    AnalyticalCell,
)


@dataclass(
    frozen=True,
    slots=True,
)
class AnalyticalBeat:
    """
    One reconstructed beat inside an
    Analytical Bar.
    """

    number: int

    cells: tuple[
        AnalyticalCell,
        ...
    ]

