from dataclasses import dataclass

from jga.domain.descriptor_set import DescriptorSet
from jga.domain.analytical_structure import AnalyticalStructure
from jga.domain.scientific_evidence_collection import (
    ScientificEvidenceCollection,
)

from jga.domain.behaviour_evolution_model import (
    BehaviourEvolutionModel,
)


@dataclass(
    frozen=True,
    slots=True,
)
class ScientificReport:
    """
    Scientific representation of a musical analysis.

    This object only aggregates validated results.
    It never recomputes analytical information.
    """

    descriptor_set: DescriptorSet

    analytical_structure: (
        AnalyticalStructure | None
    )

    scientific_evidence: (
        ScientificEvidenceCollection | None
    )

    behaviour_evolution: (
        BehaviourEvolutionModel | None
    ) = None
