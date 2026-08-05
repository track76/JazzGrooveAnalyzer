from jga.visualization.measure import (
    Measure,
)


def test_measure_can_be_created():

    measure = Measure(
        number=12,
        time_signature="4/4",
        bpm=124.3,
    )

    assert measure.number == 12

    assert measure.time_signature == "4/4"

    assert measure.bpm == 124.3
