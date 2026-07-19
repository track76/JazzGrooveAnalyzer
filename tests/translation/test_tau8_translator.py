from datetime import datetime
from uuid import uuid4

import pytest

from jga.core.metric_context import MetricContext
from jga.core.metric_source import MetricSource
from jga.core.source_pulse_sequence import SourcePulseSequence
from jga.core.pulse_candidate import PulseCandidate as CorePulseCandidate

from jga.domain.sound_source import SoundSource
from jga.domain.pulse_candidate import PulseCandidate

from jga.translation.tau8_translator import Tau8Translator


def create_metric_context():

    sequence = SourcePulseSequence(
        source=MetricSource(
            name="bass",
            family="strings",
        ),
        pulse_candidates=[
            CorePulseCandidate(
                time=1.25,
                strength=0.8,
                confidence=0.9,
            )
        ],
    )

    return MetricContext(
        source_pulse_sequences=(sequence,),
        periodicity_segments=(),
        metric_segments=(),
    )


def create_sound_source():

    return SoundSource(
        id=uuid4(),
        name="bass",
        family="strings",
        description=None,
        created_at=datetime.now(),
    )


def test_tau8_requires_metric_context():

    translator = Tau8Translator()

    with pytest.raises(ValueError):
        translator.translate(
            None,
            (),
        )


def test_tau8_requires_sound_sources():

    translator = Tau8Translator()

    with pytest.raises(ValueError):
        translator.translate(
            create_metric_context(),
            None,
        )


def test_tau8_empty_sequences_return_empty_tuple():

    translator = Tau8Translator()

    context = MetricContext(
        source_pulse_sequences=(),
        periodicity_segments=(),
        metric_segments=(
            object(),
        ),
    )

    result = translator.translate(
        context,
        (),
    )

    assert result == ()


def test_tau8_creates_domain_pulse_candidate():

    translator = Tau8Translator()

    source = create_sound_source()

    result = translator.translate(
        create_metric_context(),
        (source,),
    )

    assert len(result) == 1

    candidate = result[0]

    assert isinstance(candidate, PulseCandidate)
    assert candidate.timestamp == 1.25
    assert candidate.confidence == 0.9
    assert candidate.sound_source_id == source.id
