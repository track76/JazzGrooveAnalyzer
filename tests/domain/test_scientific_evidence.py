from jga.domain.scientific_evidence import (
    ScientificEvidence,
)


def test_creation():

    evidence = ScientificEvidence(

        name="Physical Offset",

        value=12.3,

        reference=12.0,

        delta=0.3,

        tolerance=1.0,

        compatible=True,

    )

    assert evidence.compatible

