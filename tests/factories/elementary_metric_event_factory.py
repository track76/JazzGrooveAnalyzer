from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from jga.domain.elementary_metric_event import (
    ElementaryMetricEvent,
)


def make_elementary_metric_event(
    *,
    timestamp: float = 0.0,
    confidence: float = 1.0,
) -> ElementaryMetricEvent:
    """
    Creates a valid ElementaryMetricEvent for tests.

    The generated object satisfies the complete
    Domain contract while allowing tests to
    override only the relevant values.
    """

    return ElementaryMetricEvent(
        id=uuid4(),
        contributor_id=uuid4(),
        timestamp=timestamp,
        confidence=confidence,
        created_at=datetime.now(),
    )
