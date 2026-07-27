from dataclasses import dataclass

from jga.reporting.analytical_event import (
    AnalyticalEvent,
)


@dataclass(
    frozen=True,
    slots=True,
)
class AnalyticalInstrumentRow:
    """
    One instrument row inside one bar.
    """

    instrument: str

    events: tuple[
        AnalyticalEvent,
        ...
    ]

