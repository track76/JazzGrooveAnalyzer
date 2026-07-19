from uuid import UUID

import pytest

from jga.translation.tau8_translator import Tau8Translator
from jga.core.metric_context import MetricContext


def test_tau8_requires_metric_context():

    translator = Tau8Translator()

    with pytest.raises(ValueError):
        translator.translate(None)


def test_tau8_empty_observable_sequences_return_empty_tuple():

    translator = Tau8Translator()

    context = MetricContext(
        source_pulse_sequences=(),
        periodicity_segments=(),
        metric_segments=(
            object(),
        ),
    )

    result = translator.translate(context)

    assert result == ()
