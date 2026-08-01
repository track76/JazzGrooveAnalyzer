from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class BehaviourComparisonEvidence:
    """
    Complete measurable evidence produced by
    comparing two Behaviour Observation Frames.
    """

    physical_offset_delta_ms: float

    metric_offset_delta: float

    internal_bpm_delta: float

    stability_delta: float
