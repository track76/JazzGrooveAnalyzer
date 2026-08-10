"""
Export DummyMultiStemSeparator outputs for inspection.
"""

import soundfile as sf

from jga.pipeline.default_analysis_pipeline import AnalysisPipeline
from jga.separation.dummy_multi_stem_separator import (
    DummyMultiStemSeparator,
)
from jga.operational.external_storage import ExternalStorage


INPUT = (
    "recordings/validation/"
    "03 THE COST OF LIVING versione intro + 8 bar.mp3"
)

def main():

    output = ExternalStorage.from_environment().directory(
        "stems",
        "dummy_multi_stem",
    )

    pipeline = AnalysisPipeline(
        separator=DummyMultiStemSeparator()
    )

    context = pipeline.analyze(INPUT)

    for stem in context.audio_stems:

        filename = output / f"{stem.name}.wav"

        sf.write(
            filename,
            stem.signal,
            stem.sample_rate,
        )

        print(
            "Exported:",
            filename,
            "samples:",
            stem.signal.shape,
            "sr:",
            stem.sample_rate,
        )


if __name__ == "__main__":
    main()
