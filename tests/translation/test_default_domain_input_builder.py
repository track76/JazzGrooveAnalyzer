from jga.translation.domain_input_builder import (
    DefaultDomainInputBuilder,
)

from jga.runtime.analysis_context import AnalysisContext
from jga.core.metric_context import MetricContext


def test_build_requires_metric_context():

    builder = DefaultDomainInputBuilder()

    context = AnalysisContext(audio=None)

    try:
        builder.build(context)
        assert False
    except ValueError:
        assert True


def test_build_returns_same_context_with_translation():

    builder = DefaultDomainInputBuilder()

    context = AnalysisContext(
        audio=None,
        metric_context=MetricContext(
            source_pulse_sequences=(),
            periodicity_segments=(
                object(),
            ),
            metric_segments=(),
        ),
    )

    result = builder.build(context)

    assert result is context
    assert result.elementary_metric_events == ()
