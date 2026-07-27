from jga.reporting.builders.analytical_bar_builder import (
    AnalyticalBarBuilder,
)


def test_build_preserves_temporal_boundaries():

    builder = AnalyticalBarBuilder()

    bar = builder.build(

        number=1,

        start_time_seconds=0.0,

        end_time_seconds=2.0,

        time_signature="4/4",

        internal_bpm=120.0,

    )

    assert bar.number == 1

    assert bar.start_time_seconds == 0.0

    assert bar.end_time_seconds == 2.0

    assert bar.time_signature == "4/4"

    assert bar.internal_bpm == 120.0

    assert len(bar.beats) == 0


def test_build_from_measure_preserves_reconstructed_measure_data():

    from jga.domain.reconstructed_measure import (
        ReconstructedMeasure,
    )

    from jga.reporting.builders.analytical_bar_builder import (
        AnalyticalBarBuilder,
    )


    measure = ReconstructedMeasure(

        number=3,

        time_signature="4/4",

        internal_bpm=125.0,

        start_time_seconds=4.8,

        end_time_seconds=6.72,

        beat_references=(),

        metric_clusters=(),

    )


    builder = AnalyticalBarBuilder()


    bar = builder.build_from_measure(
        measure
    )


    assert bar.number == 3

    assert bar.start_time_seconds == 4.8

    assert bar.end_time_seconds == 6.72

    assert bar.time_signature == "4/4"

    assert bar.internal_bpm == 125.0


def test_build_from_measure_populates_analytical_beats():

    from datetime import datetime
    from uuid import uuid4

    from jga.domain.beat_reference import (
        BeatReference,
    )

    from jga.domain.reconstructed_measure import (
        ReconstructedMeasure,
    )

    from jga.reporting.builders.analytical_bar_builder import (
        AnalyticalBarBuilder,
    )


    measure = ReconstructedMeasure(

        number=1,

        time_signature="4/4",

        internal_bpm=120.0,

        start_time_seconds=0.0,

        end_time_seconds=2.0,

        beat_references=(

            BeatReference(
                id=uuid4(),
                index=0,
                timestamp=0.0,
                created_at=datetime.now(),
            ),

            BeatReference(
                id=uuid4(),
                index=1,
                timestamp=0.5,
                created_at=datetime.now(),
            ),

            BeatReference(
                id=uuid4(),
                index=2,
                timestamp=1.0,
                created_at=datetime.now(),
            ),

            BeatReference(
                id=uuid4(),
                index=3,
                timestamp=1.5,
                created_at=datetime.now(),
            ),

        ),

        metric_clusters=(),

    )


    builder = AnalyticalBarBuilder()


    bar = builder.build_from_measure(
        measure
    )


    assert len(bar.beats) == 4

    assert bar.beats[0].number == 1

    assert (
        bar.beats[0].timestamp_seconds
        == 0.0
    )

    assert bar.beats[3].number == 4

    assert (
        bar.beats[3].timestamp_seconds
        == 1.5
    )
