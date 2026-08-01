
from jga.domain.behaviour_comparison_evidence import (
    BehaviourComparisonEvidence,
)

from jga.domain.behaviour_evidence_summary import (
    BehaviourEvidenceSummary,
)


class BehaviourEvidenceAggregator:
    """
    Aggregates primitive BehaviourComparisonEvidence
    into a consolidated BehaviourEvidenceSummary.
    """

    def aggregate(
        self,
        evidences: tuple[
            BehaviourComparisonEvidence,
            ...
        ],
    ) -> BehaviourEvidenceSummary:

        count = len(evidences)

        if count == 0:
            return BehaviourEvidenceSummary(
                comparison_count=0,
                mean_physical_offset_delta_ms=0.0,
                mean_metric_offset_delta=0.0,
                mean_internal_bpm_delta=0.0,
                mean_stability_delta=0.0,
            )

        return BehaviourEvidenceSummary(
            comparison_count=count,
            mean_physical_offset_delta_ms=(
                sum(
                    e.physical_offset_delta_ms
                    for e in evidences
                )
                / count
            ),
            mean_metric_offset_delta=(
                sum(
                    e.metric_offset_delta
                    for e in evidences
                )
                / count
            ),
            mean_internal_bpm_delta=(
                sum(
                    e.internal_bpm_delta
                    for e in evidences
                )
                / count
            ),
            mean_stability_delta=(
                sum(
                    e.stability_delta
                    for e in evidences
                )
                / count
            ),
        )

