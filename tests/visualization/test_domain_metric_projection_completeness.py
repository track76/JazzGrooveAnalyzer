"""
Domain Metric Projection Completeness.

Verifies that every ElementaryMetricEvent
is projected exactly once and in temporal order.
"""

from datetime import datetime
from uuid import uuid4

from jga.domain.beat_reference import BeatReference
from jga.domain.elementary_metric_event import ElementaryMetricEvent
from jga.domain.internal_metric_timeline import InternalMetricTimeline
from jga.domain.metric_cluster import MetricCluster
from jga.domain.pulse import Pulse
from jga.visualization.domain_metric_projector import (
    DomainMetricProjector,
)


def test_projection_preserves_event_order_and_cardinality():
    events = (
        ElementaryMetricEvent(
            id=uuid4(),
            contributor_id=uuid4(),
            timestamp=1.0,
            confidence=0.90,
            created_at=datetime.now(),
        ),
        ElementaryMetricEvent(
            id=uuid4(),
            contributor_id=uuid4(),
            timestamp=2.0,
            confidence=0.80,
            created_at=datetime.now(),
        ),
    )

    beat = BeatReference(
        id=uuid4(),
        index=0,
        timestamp=1.0,
        created_at=datetime.now(),
    )

    cluster = MetricCluster(
        id=uuid4(),
        beat_reference=beat,
        events=events,
        created_at=datetime.now(),
    )

    pulse = Pulse(
        id=uuid4(),
        index=0,
        cluster=cluster,
        timestamp=1.0,
        created_at=datetime.now(),
    )

    timeline = InternalMetricTimeline(
        id=uuid4(),
        pulses=(pulse,),
        created_at=datetime.now(),
    )

    series = DomainMetricProjector().project(timeline)

    assert len(series.points) == len(events)

    assert [p.time for p in series.points] == [1.0, 2.0]

    assert [p.value for p in series.points] == [0.90, 0.80]
