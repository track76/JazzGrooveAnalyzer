from jga.domain.scientific_evidence import (
    ScientificEvidence,
)

from jga.domain.scientific_evidence_collection import (
    ScientificEvidenceCollection,
)


def test_scientific_evidence_collection():

    evidence = ScientificEvidence(
        name="stability",
        value=0.1,
        reference=0.0,
        delta=0.1,
        tolerance=0.05,
        compatible=False,
    )

    collection = ScientificEvidenceCollection(
        evidences=(evidence,)
    )

    assert len(collection.evidences) == 1
    assert collection.evidences[0].name == "stability"
