from pathlib import Path

from jga.audio.file_audio_source import FileAudioSource
from jga.runtime.analysis_context import AnalysisContext
from jga.separation.demucs_separator import (
    DemucsSeparator,
)
from jga.separation.demucs_runner import (
    DemucsRunner,
)


def test_m31_real_demucs_separator_creates_stems():

    audio_path = Path(
        "recordings/III_Chet Baker - I fall in love too easily.mp3"
    )

    assert audio_path.exists()

    audio = FileAudioSource().load(
        str(audio_path)
    )

    context = AnalysisContext(
        audio=audio
    )

    separator = DemucsSeparator(
        runner=DemucsRunner(
            executable="/Users/StarTrack/Development/JGA-Demucs-env/bin/demucs"
        )
    )

    context = separator.process(
        context
    )

    assert context.audio_stems is not None

    names = {
        stem.name
        for stem in context.audio_stems
    }

    assert "bass" in names
    assert "drums" in names
    assert "other" in names
    assert "vocals" in names

    assert len(
        context.audio_stems
    ) == 4

    for stem in context.audio_stems:
        assert stem.signal is not None
        assert stem.sample_rate > 0
        assert stem.source == "DemucsSeparator"
