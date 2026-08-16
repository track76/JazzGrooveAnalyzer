from dataclasses import FrozenInstanceError
from decimal import Decimal

import pytest

from jga.domain.declared_metric_reference import (
    DeclaredMetricReference,
    MetricReferenceProvenance,
)
from jga.interfaces.scientific_value_origin import ScientificValueOrigin


def provenance() -> MetricReferenceProvenance:
    return MetricReferenceProvenance(
        source_id="CONTROLLED-CONTEXT-TEST",
        source_kind="authoritative_controlled_source_context",
        source_sha256="a" * 64,
        temporal_scope="complete_recording",
    )


def test_declared_metric_reference_is_immutable_and_preserves_origin():
    reference = DeclaredMetricReference(
        beats_per_minute=Decimal("78"),
        beat_unit="quarter",
        provenance=provenance(),
    )

    assert reference.origin is ScientificValueOrigin.DECLARED
    assert reference.period_seconds == Decimal("60") / Decimal("78")
    with pytest.raises(FrozenInstanceError):
        reference.beats_per_minute = Decimal("120")


@pytest.mark.parametrize("value", [Decimal("0"), Decimal("-1")])
def test_declared_metric_reference_requires_positive_bpm(value):
    with pytest.raises(ValueError, match="positive"):
        DeclaredMetricReference(value, "quarter", provenance())


def test_metric_reference_provenance_requires_sha256_identity():
    with pytest.raises(ValueError, match="SHA-256"):
        MetricReferenceProvenance(
            source_id="CONTROLLED-CONTEXT-TEST",
            source_kind="authoritative_controlled_source_context",
            source_sha256="not-a-checksum",
            temporal_scope="complete_recording",
        )
