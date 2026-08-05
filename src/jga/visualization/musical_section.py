"""
Musical Section.

Represents one formal section of a musical composition
within the Analytical Score.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MusicalSection:
    """
    Immutable musical section.
    """

    name: str

    first_measure: int

    last_measure: int
