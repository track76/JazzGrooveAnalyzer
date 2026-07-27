from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class AnalyticalEvent:
    """
    One detected event represented in the
    Analytical Score.
    """

    beat: int

    cluster_index: int

    offset_ms: float

    delta_ms: float

    significant_change: bool

