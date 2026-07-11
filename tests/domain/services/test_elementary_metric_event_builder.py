from datetime import datetime
from uuid import uuid4

import pytest

from jga.domain.elementary_metric_event import ElementaryMetricEvent
from jga.domain.services.elementary_metric_event_builder import (
    ElementaryMetricEventBuilder,
)


def test_builder_can_be_instantiated():
    builder = ElementaryMetricEventBuilder()

    assert builder is not None


def test_build_requires_argument():
    builder = ElementaryMetricEventBuilder()

    with pytest.raises(TypeError):
        builder.build()


def test_build_returns_empty_tuple_when_no_intervals():
    builder = ElementaryMetricEventBuilder()

    events = builder.build(())

    assert events == ()