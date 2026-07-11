"""
=========================================================
Jazz Groove Analyzer (JGA)

Transient Observation Object

Copyright © 2026 Angelo Tracanna
=========================================================
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Transient:
    """
    Observable transient event.

    A transient is a short-duration variation of the audio signal,
    potentially associated with the beginning of a sound event.

    This object belongs to the Observation Domain and contains
    only observable information extracted from the audio signal.
    """

    time: float