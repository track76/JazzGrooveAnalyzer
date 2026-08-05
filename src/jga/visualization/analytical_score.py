"""
Analytical Score.

Immutable representation of the musicological analytical score
produced by the Jazz Groove Analyzer.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AnalyticalScore:
    """
    Musicological analytical score.

    This object represents the complete analytical score before
    graphical rendering.
    """

    recording_title: str

    artist: str

    time_signature: str

    average_bpm: float

    sections: tuple

    measures: tuple

    instrument_lanes: tuple
