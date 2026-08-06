from jga.semantics.builders.metric_event_semantics_builder import (
    MetricEventSemanticsBuilder,
)
from jga.semantics.metric_event_semantics import (
    MetricEventSemantics,
)


def test_builder_returns_semantics():

    semantics = (
        MetricEventSemanticsBuilder()
        .build()
    )

    assert isinstance(
        semantics,
        MetricEventSemantics,
    )
