from pathlib import Path

from jga.audio.file_audio_source import FileAudioSource
from jga.engines.audio_preprocessor import AudioPreprocessor
from jga.engines.candidate_period_discovery import CandidatePeriodDiscovery
from jga.engines.pulse_candidate_builder import PulseCandidateBuilder
from jga.engines.pulse_candidate_filter import PulseCandidateFilter
from jga.pipeline.default_analysis_pipeline import AnalysisPipeline
from jga.runtime.analysis_context import AnalysisContext
from jga.separation.dummy_multi_stem_separator import DummyMultiStemSeparator


FULL_MIX = Path(
    "recordings/validation/03 THE COST OF LIVING versione intro + 8 bar.mp3"
)
STEM_EXPECTATIONS = {
    Path("recordings/validation/stems/double_bass.wav"): {
        33: 8,
        132: 2,
        232: 6,
        265: 2,
    },
    Path("recordings/validation/stems/drums.wav"): {
        30: 7,
        33: 19,
        37: 3,
        66: 15,
        67: 6,
        70: 3,
    },
    Path("recordings/validation/stems/piano.wav"): {
        17: 4,
        32: 5,
        33: 6,
        34: 13,
        65: 5,
        66: 3,
        100: 2,
        132: 3,
        165: 2,
        166: 4,
    },
    Path("recordings/validation/stems/tenor_sax.wav"): {
        3: 2,
        265: 2,
    },
    Path("recordings/validation/stems/voice.wav"): {
        3: 10,
        4: 12,
        5: 7,
        6: 13,
        7: 5,
        8: 5,
        9: 8,
        10: 6,
        11: 10,
        12: 11,
        13: 7,
        14: 4,
        15: 5,
        16: 5,
        17: 5,
        18: 3,
        19: 4,
        20: 6,
        21: 3,
        22: 2,
        23: 2,
        24: 3,
        32: 3,
    },
}
FULL_MIX_EXPECTATION = {
    3: 3,
    31: 9,
    32: 9,
    33: 16,
    34: 7,
    35: 2,
    36: 3,
    64: 2,
    66: 8,
    67: 2,
    69: 5,
    101: 2,
}


def _frame_inventory(context: AnalysisContext) -> dict[int, int]:
    population = context.candidate_period_population
    configuration = dict(population.provenance.discovery_configuration)
    frame_length = int(configuration["frame_length_samples"])
    sample_rate = int(configuration["sample_rate_hz"])
    return {
        round(float(period.duration_seconds) * sample_rate / frame_length): len(
            period.recurrence_evidence
        )
        for period in population.candidates
    }


def _observe(path: Path) -> AnalysisContext:
    audio = FileAudioSource().load(path.as_posix())
    context = AnalysisContext(audio=audio)
    AudioPreprocessor().process(context)
    detector = PulseCandidateBuilder()
    detector.process(context)
    PulseCandidateFilter().process(context)
    CandidatePeriodDiscovery(
        frame_length_samples=detector.FRAME_LENGTH_SAMPLES
    ).process(context)
    return context


def test_full_pipeline_preserves_complete_val_001_population() -> None:
    context = AnalysisPipeline(
        separator=DummyMultiStemSeparator()
    ).analyze(FULL_MIX.as_posix())

    assert _frame_inventory(context) == FULL_MIX_EXPECTATION
    assert context.candidate_period_population.provenance.source_revision is None


def test_controlled_wavs_preserve_accepted_candidate_populations() -> None:
    for path, expected in STEM_EXPECTATIONS.items():
        context = _observe(path)

        assert _frame_inventory(context) == expected
        assert context.candidate_period_population.provenance.input_asset_path == (
            path.as_posix()
        )
