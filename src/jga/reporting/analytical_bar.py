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

    Analytical representation of a ReconstructedMeasure.
    Temporal boundaries are preserved from the scientific
    reconstruction layer.
    """

    number: int

    start_time_seconds: float

    end_time_seconds: float

    time_signature: str

    internal_bpm: float

    beats: tuple[
        AnalyticalBeat,
        ...
    ]
