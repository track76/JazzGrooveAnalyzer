from dataclasses import is_dataclass

from jga.domain.boundary_evidence import BoundaryEvidence


def test_boundary_evidence_is_dataclass():

    assert is_dataclass(BoundaryEvidence)


def test_boundary_evidence_is_immutable():

    evidence = BoundaryEvidence(
        observation_index=42,
    )

    assert evidence.observation_index == 42
