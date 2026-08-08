"""
Export DummyMultiStemSeparator outputs for inspection.
"""

from pathlib import Path

import soundfile as sf

from jga.pipeline.default_analysis_pipeline import AnalysisPipeline
from jga.separation.dummy_multi_stem_separator import (
    DummyMultiStemSeparator,
)


INPUT = (
    "recordings/validation/"
    "03 THE COST OF LIVING versione intro + 8 bar.mp3"
)

OUTPUT = Path("output/dummy_stems")


def main():

    pipeline = AnalysisPipeline(
        separator=DummyMultiStemSeparator()
    )

    context = pipeline.analyze(INPUT)

    OUTPUT.mkdir(
        parents=True,
        exist_ok=True,
    )

    for stem in context.audio_stems:

        filename = OUTPUT / f"{stem.name}.wav"

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
