from pathlib import Path

from jga.audio.file_audio_source import FileAudioSource
from jga.core.audio_stem import AudioStem
from jga.core.audio_stem_collection import AudioStemCollection
from jga.source_understanding.classifiers.default_classifier_registry import (
    DefaultClassifierRegistry,
)
from jga.source_understanding.services.source_understanding_service import (
    SourceUnderstandingService,
)


def test_source_understanding_real_audio_validation():

    audio_path = Path(
        "recordings/III_Chet Baker - I fall in love too easily.mp3"
    )

    audio_file = FileAudioSource().load(
        str(audio_path)
    )

    signal = audio_file.raw_audio

    if signal.ndim > 1:
        signal = signal[0]

    stem = AudioStem(
        name="audio",
        signal=signal,
        sample_rate=audio_file.sample_rate,
    )

    stems = AudioStemCollection(
        (stem,)
    )

    service = SourceUnderstandingService(
        classifier=DefaultClassifierRegistry(),
    )

    observed = service.process(stems)

    assert len(observed) == 1

    classification = observed[0].classification

    assert classification is not None
    assert classification.confidence >= 0.0
