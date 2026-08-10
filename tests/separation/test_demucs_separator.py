from pathlib import Path

import numpy as np
import pytest
import soundfile as sf

from jga.core.audio_file import AudioFile
from jga.runtime.analysis_context import AnalysisContext
from jga.separation.demucs_separator import (
    DemucsSeparator,
)


def make_context():

    audio = AudioFile(
        path=Path("dummy.mp3"),
        raw_audio=np.array([]),
        sample_rate=44100,
        duration=10.0,
        channels=1,
        format="mp3",
    )

    return AnalysisContext(
        audio=audio
    )


class FakeDemucsRunner:

    def separate(
        self,
        input_file,
        output_directory,
    ):

        output = (
            Path(output_directory)
            / "htdemucs"
            / input_file.stem
        )

        output.mkdir(
            parents=True,
        )

        signal = np.zeros(
            44100,
            dtype=np.float32,
        )

        for name in (
            "bass",
            "drums",
            "other",
        ):
            sf.write(
                output / f"{name}.wav",
                signal,
                44100,
            )

        return output


def test_demucs_separator_creates_audio_stem_collection(
    monkeypatch,
    tmp_path,
):

    monkeypatch.setenv(
        "JGA_EXTERNAL_ROOT",
        str(tmp_path),
    )

    context = make_context()

    separator = DemucsSeparator(
        runner=FakeDemucsRunner()
    )

    context = separator.process(
        context
    )

    assert context.audio_stems is not None

    assert len(
        context.audio_stems
    ) == 3

    names = {
        stem.name
        for stem in context.audio_stems
    }

    assert names == {
        "bass",
        "drums",
        "other",
    }

    for stem in context.audio_stems:
        assert stem.source == "DemucsSeparator"


def test_demucs_separator_fails_closed_without_external_storage(
    monkeypatch,
):

    monkeypatch.delenv("JGA_EXTERNAL_ROOT", raising=False)

    separator = DemucsSeparator(
        runner=FakeDemucsRunner()
    )

    with pytest.raises(
        RuntimeError,
        match="heavy default writes are disabled",
    ):
        separator.process(make_context())
