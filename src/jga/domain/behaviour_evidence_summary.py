
from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class BehaviourEvidenceSummary:
    """
    Consolidated behavioural evidence summary.

    Represents aggregated measurable evidence
    derived from multiple BehaviourComparisonEvidence
    observations.
    """

    comparison_count: int

    mean_physical_offset_delta_ms: float

    mean_metric_offset_delta: float

    mean_internal_bpm_delta: float

    mean_stability_delta: float

    @property
    def is_stable(self) -> bool:
        return (
            self.mean_physical_offset_delta_ms == 0.0
            and self.mean_metric_offset_delta == 0.0
            and self.mean_internal_bpm_delta == 0.0
            and self.mean_stability_delta == 0.0
        )

