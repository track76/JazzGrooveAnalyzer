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

    album: str = ""

    take: str = ""

    year: str = ""

    time_signature: str = ""

    meter_origin: str | None = None

    meter_source_id: str | None = None

    average_bpm: float = 0.0

    metric_reference_origin: str | None = None

    metric_reference_beat_unit: str | None = None

    metric_reference_source_id: str | None = None

    duration: float = 0.0

    sections: tuple = ()

    measures: tuple = ()

    instrument_lanes: tuple = ()
