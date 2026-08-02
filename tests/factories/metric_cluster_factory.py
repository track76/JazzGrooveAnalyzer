from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from jga.domain.beat_reference import (
    BeatReference,
)

from jga.domain.metric_cluster import (
    MetricCluster,
)

from tests.factories.elementary_metric_event_factory import (
    make_elementary_metric_event,
)


def make_metric_cluster() -> MetricCluster:
    """
    Creates a valid MetricCluster for tests.
    """

    event = make_elementary_metric_event()

    beat_reference = BeatReference(
        id=uuid4(),
        index=0,
        timestamp=event.timestamp,
        created_at=datetime.now(),
    )

    return MetricCluster(
        id=uuid4(),
        beat_reference=beat_reference,
        events=(
            event,
        ),
        created_at=datetime.now(),
    )
