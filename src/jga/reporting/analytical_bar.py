from dataclasses import dataclass

from jga.reporting.analytical_beat import (
    AnalyticalBeat,
)


@dataclass(
    frozen=True,
    slots=True,
)
class AnalyticalBar:
    """
    One reconstructed musical bar.
    """

    number: int

    time_seconds: float

    time_signature: str

    internal_bpm: float

    beats: tuple[
        AnalyticalBeat,
        ...
    ]

