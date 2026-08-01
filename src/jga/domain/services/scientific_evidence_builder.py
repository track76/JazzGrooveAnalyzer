from jga.domain.behaviour_comparison_evidence import (
    BehaviourComparisonEvidence,
)

from jga.domain.scientific_evidence import (
    ScientificEvidence,
)

from jga.domain.scientific_evidence_collection import (
    ScientificEvidenceCollection,
)


class ScientificEvidenceBuilder:
    """
    Builds ScientificEvidence from measurable
    Behaviour Comparison Evidence.
    """

    def build(
        self,
        evidence: BehaviourComparisonEvidence,
    ) -> ScientificEvidenceCollection:

        return ScientificEvidenceCollection(
            evidences=(
                ScientificEvidence(
                name="physical_offset",
                value=evidence.physical_offset_delta_ms,
                reference=0.0,
                delta=evidence.physical_offset_delta_ms,
                tolerance=0.0,
                compatible=(
                    evidence.physical_offset_delta_ms == 0.0
                ),
            ),

            ScientificEvidence(
                name="metric_offset",
                value=evidence.metric_offset_delta,
                reference=0.0,
                delta=evidence.metric_offset_delta,
                tolerance=0.0,
                compatible=(
                    evidence.metric_offset_delta == 0.0
                ),
            ),

            ScientificEvidence(
                name="internal_bpm",
                value=evidence.internal_bpm_delta,
                reference=0.0,
                delta=evidence.internal_bpm_delta,
                tolerance=0.0,
                compatible=(
                    evidence.internal_bpm_delta == 0.0
                ),
            ),

            ScientificEvidence(
                name="stability",
                value=evidence.stability_delta,
                reference=0.0,
                delta=evidence.stability_delta,
                tolerance=0.0,
                compatible=(
                    evidence.stability_delta == 0.0
                ),
                ),
            )
        )
