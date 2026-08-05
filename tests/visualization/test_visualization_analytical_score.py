from jga.visualization.analytical_score import (
    AnalyticalScore,
)


def test_analytical_score_can_be_instantiated():

    score = AnalyticalScore(
        recording_title="",
        artist="",
        time_signature="4/4",
        average_bpm=120.0,
        sections=(),
        measures=(),
        instrument_lanes=(),
    )

    assert score.recording_title == ""


def test_analytical_score_stores_recording_metadata():

    score = AnalyticalScore(
        recording_title="I Fall In Love Too Easily",
        artist="Chet Baker",
        time_signature="4/4",
        average_bpm=124.0,
        sections=(),
        measures=(),
        instrument_lanes=(),
    )

    assert score.recording_title == (
        "I Fall In Love Too Easily"
    )

    assert score.artist == (
        "Chet Baker"
    )

    assert score.time_signature == "4/4"

    assert score.average_bpm == 124.0


from jga.visualization.instrument_lane import (
    InstrumentLane,
)
from jga.visualization.measure import (
    Measure,
)
from jga.visualization.musical_section import (
    MusicalSection,
)


def test_analytical_score_aggregates_score_structure():

    sections = (
        MusicalSection(
            name="Intro",
            first_measure=1,
            last_measure=8,
        ),
    )

    measures = (
        Measure(
            number=1,
            time_signature="4/4",
            bpm=124.0,
        ),
    )

    lanes = (
        InstrumentLane(
            name="Bass",
        ),
    )

    score = AnalyticalScore(
        recording_title="I Fall In Love Too Easily",
        artist="Chet Baker",
        time_signature="4/4",
        average_bpm=124.0,
        sections=sections,
        measures=measures,
        instrument_lanes=lanes,
    )

    assert score.sections == sections

    assert score.measures == measures

    assert score.instrument_lanes == lanes
