"""
Measure.

Represents one measure of the Analytical Score.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Measure:
    """
    Immutable measure representation.
    """

    number: int

    time_signature: str

    bpm: float
