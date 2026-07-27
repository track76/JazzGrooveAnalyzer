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

    The timestamp preserves the temporal identity
    of the source BeatReference.
    """

    number: int

    timestamp_seconds: float

    cells: tuple[
        AnalyticalCell,
        ...
    ]
