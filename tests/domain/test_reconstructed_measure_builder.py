from datetime import datetime
from uuid import uuid4

from jga.domain.beat_reference import (
    BeatReference,
)

from jga.domain.internal_metric_signature import (
    InternalMetricSignature,
)

from jga.domain.services.reconstructed_measure_builder import (
    ReconstructedMeasureBuilder,
)


def create_beat(index: int):

    return BeatReference(

        id=uuid4(),

        index=index,

        timestamp=float(index),

        created_at=datetime.now(),

    )


def test_empty_sequence():

    builder = ReconstructedMeasureBuilder()

    result = builder.build(

        beat_references=(),

        metric_signature=InternalMetricSignature(
            numerator=4,
            denominator=4,
        ),

        internal_bpm=120.0,

    )

    assert result == ()


def test_reconstruct_two_measures():

    builder = ReconstructedMeasureBuilder()

    beats = tuple(
        create_beat(index)
        for index in range(32)
    )

    measures = builder.build(

        beat_references=beats,

        metric_signature=InternalMetricSignature(
            numerator=4,
            denominator=4,
        ),

        internal_bpm=120.0,

    )

    assert len(measures) == 2

    assert measures[0].number == 1

    assert measures[1].number == 2

    assert len(measures[0].beat_references) == 16

    assert len(measures[1].beat_references) == 16

