"""
Measure Block.

Visual container for grouped measures
in Analytical Groove Score rendering.

Copyright © 2026 Angelo Tracanna
"""

from dataclasses import dataclass

from jga.visualization.measure import Measure


@dataclass(frozen=True, slots=True)
class MeasureBlock:
    """
    Group of measures rendered together.
    """

    measures: tuple[Measure, ...]

    section: str = ""

    @property
    def start_measure(self) -> int:
        return self.measures[0].number

    @property
    def end_measure(self) -> int:
        return self.measures[-1].number
