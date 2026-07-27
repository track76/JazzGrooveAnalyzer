from jga.domain.internal_metric_signature import (
    InternalMetricSignature,
)


def test_signature():

    signature = InternalMetricSignature(

        numerator=4,

        denominator=4,

    )

    assert signature.beats_per_measure == 4

    assert str(signature) == "4/4"

