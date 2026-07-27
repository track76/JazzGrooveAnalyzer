from dataclasses import dataclass

from jga.reporting.analytical_bar import (
    AnalyticalBar,
)


@dataclass(
    frozen=True,
    slots=True,
)
class AnalyticalScore:
    """
    Complete analytical representation of one
    musical performance.
    """

    title: str

    artist: str

    bars: tuple[
        AnalyticalBar,
        ...
    ]

