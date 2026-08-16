from dataclasses import FrozenInstanceError

import pytest

from jga.domain.declared_meter import DeclaredMeter
from jga.domain.declared_metric_reference import MetricReferenceProvenance
from jga.interfaces.scientific_value_origin import ScientificValueOrigin


def provenance() -> MetricReferenceProvenance:
    return MetricReferenceProvenance(
        source_id="CONTROLLED-CONTEXT-TEST",
        source_kind="authoritative_controlled_source_context",
        source_sha256="a" * 64,
        temporal_scope="complete_recording",
    )


def test_declared_meter_is_immutable_and_preserves_origin():
    meter = DeclaredMeter(4, 4, provenance())

    assert meter.origin is ScientificValueOrigin.DECLARED
    assert str(meter) == "4/4"
    with pytest.raises(FrozenInstanceError):
        meter.numerator = 3


@pytest.mark.parametrize(
    ("numerator", "denominator"),
    ((0, 4), (-1, 4), (4, 0), (4, -1)),
)
def test_declared_meter_requires_positive_components(numerator, denominator):
    with pytest.raises(ValueError, match="positive"):
        DeclaredMeter(numerator, denominator, provenance())
