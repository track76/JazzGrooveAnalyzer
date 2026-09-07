"""Synthetic API diagnostic only: no scientific input or acceptance execution."""

from pathlib import Path

import numpy as np
from librosa.util.exceptions import ParameterError

from jga.core.audio_file import AudioFile
from jga.core.audio_stem import AudioStem
from jga.core.audio_stem_collection import AudioStemCollection
from jga.engines.source_pulse_candidate_builder import SourcePulseCandidateBuilder
from jga.runtime.analysis_context import AnalysisContext


def main():
    signal = np.zeros((2, 44100), dtype=np.float32)
    signal[:, 10000:10010] = 1
    context = AnalysisContext(
        audio=AudioFile(Path("synthetic.wav"), signal, 44100, 1.0, 2, "wav")
    )
    context.audio_stems = AudioStemCollection((
        AudioStem(name="drums", signal=signal, sample_rate=44100),
    ))
    try:
        SourcePulseCandidateBuilder().process(context)
    except ParameterError as exc:
        assert "sparse=True" in str(exc) and "2-dimensional" in str(exc)
        print(f"CONFIRMED_STEREO_HANDOFF_BLOCKER: {exc}")
    else:
        raise AssertionError("Diagnostic no longer reproduces; re-audit required")


if __name__ == "__main__":
    main()
