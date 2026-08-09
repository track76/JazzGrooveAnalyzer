from dataclasses import FrozenInstanceError
from decimal import Decimal

import numpy as np
from pytest import raises

from jga.core.audio_file import AudioFile
from jga.core.pulse_candidate import PulseCandidate
from jga.engines.candidate_period_discovery import CandidatePeriodDiscovery
from jga.runtime.analysis_context import AnalysisContext


def _context(tmp_path) -> AnalysisContext:
    asset = tmp_path / "observation.wav"
    asset.write_bytes(b"candidate-period-test")
    audio = AudioFile(
        path=asset,
        raw_audio=np.zeros(4096),
        sample_rate=1024,
        duration=4.0,
        channels=1,
        format="wav",
    )
    return AnalysisContext(
        audio=audio,
        pulse_candidates=[
            PulseCandidate(time=0.0, strength=1.0),
            PulseCandidate(time=0.5, strength=1.0),
            PulseCandidate(time=1.0, strength=1.0),
            PulseCandidate(time=2.0, strength=1.0),
            PulseCandidate(time=3.0, strength=1.0),
        ],
    )


def test_discovers_complete_recurrent_consecutive_population(tmp_path) -> None:
    context = _context(tmp_path)

    CandidatePeriodDiscovery(frame_length_samples=512).process(context)

    population = context.candidate_period_population
    assert population.measurement_unit == "seconds"
    assert tuple(period.duration_seconds for period in population.candidates) == (
        Decimal("0.5"),
        Decimal("1.0"),
    )
    assert tuple(
        len(period.recurrence_evidence) for period in population.candidates
    ) == (2, 2)


def test_discovery_is_deterministic(tmp_path) -> None:
    first = _context(tmp_path)
    second = _context(tmp_path)
    discovery = CandidatePeriodDiscovery(frame_length_samples=512)

    discovery.process(first)
    discovery.process(second)

    assert first.candidate_period_population == second.candidate_period_population


def test_discovery_preserves_explicit_configuration_and_runtime_provenance(
    tmp_path,
) -> None:
    context = _context(tmp_path)

    CandidatePeriodDiscovery(frame_length_samples=512).process(context)

    population = context.candidate_period_population
    assert population.provenance.source_revision is None
    assert population.provenance.input_asset_path.endswith("observation.wav")
    assert len(population.provenance.input_asset_sha256) == 64
    assert population.provenance.discovery_configuration == (
        ("frame_length_samples", "512"),
        ("sample_rate_hz", "1024"),
        (
            "recurrence_definition",
            "exact consecutive positive frame interval occurring at least twice",
        ),
    )


def test_discovery_output_is_deeply_immutable(tmp_path) -> None:
    context = _context(tmp_path)
    CandidatePeriodDiscovery(frame_length_samples=512).process(context)
    population = context.candidate_period_population

    with raises(FrozenInstanceError):
        population.measurement_unit = "frames"
    with raises(FrozenInstanceError):
        population.candidates[0].duration_seconds = Decimal("2")
    with raises(FrozenInstanceError):
        population.candidates[0].recurrence_evidence[0].end_seconds = Decimal(
            "2"
        )


def test_discovery_ignores_non_positive_consecutive_intervals(tmp_path) -> None:
    context = _context(tmp_path)
    context.pulse_candidates = [
        PulseCandidate(time=0.5, strength=1.0),
        PulseCandidate(time=0.5, strength=1.0),
    ]

    CandidatePeriodDiscovery(frame_length_samples=512).process(context)

    assert context.candidate_period_population.candidates == ()
