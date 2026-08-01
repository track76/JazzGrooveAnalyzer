
from pathlib import Path

from jga.pipeline.default_analysis_pipeline import (
    AnalysisPipeline,
)


def test_m30_real_mp3_creates_audio_stems():

    audio_path = Path(
        "recordings/III_Chet Baker - I fall in love too easily.mp3"
    )

    assert audio_path.exists()

    pipeline = AnalysisPipeline()

    context = pipeline.analyze(
        str(audio_path)
    )

    assert context.audio_stems is not None

    assert len(context.audio_stems) == 1

    stem = context.audio_stems[0]

    assert stem.source == (
        "NullSeparator"
    )

    assert stem.sample_rate == (
        context.audio.sample_rate
    )
