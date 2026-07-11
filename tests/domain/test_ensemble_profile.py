from jga.domain.ensemble_profile import EnsembleProfile


def test_ensemble_profile_creation():

    profile = EnsembleProfile(
        meter="4/4",
        estimated_bpm=120.0,
        pulse_start=3.25,
        sound_sources=[],
        musical_functions=[],
        metric_contributors=[],
        confidence=0.98,
    )

    assert profile.meter == "4/4"
    assert profile.estimated_bpm == 120.0
    assert profile.confidence == 0.98