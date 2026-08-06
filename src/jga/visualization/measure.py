"""
Measure.

Represents one measure of the Analytical Score.
"""

from dataclasses import dataclass

from jga.visualization.metric_event import (
    MetricEvent,
)


@dataclass(frozen=True, slots=True)
class Measure:
    """
    Immutable measure representation.
    """

    number: int

    time_signature: str

    bpm: float

    title: str = ""

    composer: str = ""

    section: str = ""

    software_name: str = "JazzGrooveAnalyzer"

    software_author: str = "Angelo Tracanna"

    copyright: str = "Copyright © 2026 Angelo Tracanna"

    theoretical_beats: tuple[float, ...] = ()

    beat_positions: tuple[float, ...] = ()

    start_time_seconds: float = 0.0

    metric_events: tuple[MetricEvent, ...] = ()
