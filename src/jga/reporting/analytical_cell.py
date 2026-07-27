from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class AnalyticalCell:
    """
    One analytical observation displayed inside
    one Beat of one Bar.

    Each cell represents the temporal position
    of one detected musical event with respect
    to the reconstructed Internal Timing.
    """

    instrument: str

    beat: int

    metric_cluster_id: int

    absolute_time_seconds: float

    internal_bpm: float

    offset_ms: float

    delta_ms: float

    significant_change: bool

