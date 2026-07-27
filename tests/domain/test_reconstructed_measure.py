from jga.domain.reconstructed_measure import (
    ReconstructedMeasure,
)


def test_creation():

    measure = ReconstructedMeasure(

        number=1,

        time_signature="4/4",

        internal_bpm=120.0,

        start_time_seconds=0.0,

        end_time_seconds=2.0,

        beat_references=(),

        metric_clusters=(),

    )

    assert measure.number == 1

    assert measure.time_signature == "4/4"

    assert measure.internal_bpm == 120.0

