from jga.source_understanding.ensemble_profile import EnsembleProfile
from jga.source_understanding.instrument_family import InstrumentFamily


def test_ensemble_profile_creation():
    profile = EnsembleProfile(
        families=(
            InstrumentFamily.BASS,
            InstrumentFamily.PERCUSSION,
            InstrumentFamily.CHORDAL,
        ),
        confidence=0.95,
    )

    assert profile.size == 3
    assert profile.confidence == 0.95
    assert InstrumentFamily.BASS in profile.families


def test_empty_ensemble():
    profile = EnsembleProfile(
        families=(),
        confidence=0.0,
    )

    assert profile.size == 0
