import pytest

from datetime import datetime
from uuid import uuid4

from jga.domain.beat_reference import BeatReference
from jga.domain.elementary_metric_event import ElementaryMetricEvent
from jga.domain.metric_cluster import MetricCluster

from jga.reporting.builders.analytical_cell_builder import (
    AnalyticalCellBuilder,
)


def test_build_from_metric_cluster_event():

    beat_reference = BeatReference(
        id=uuid4(),
        index=4,
        timestamp=1.0,
        created_at=datetime.now(),
    )

    event = ElementaryMetricEvent(
        id=uuid4(),
        contributor_id=uuid4(),
        timestamp=1.012,
        confidence=1.0,
        created_at=datetime.now(),
    )

    cluster_id = uuid4()

    cluster = MetricCluster(
        id=cluster_id,
        beat_reference=beat_reference,
        events=(event,),
        created_at=datetime.now(),
    )

    builder = AnalyticalCellBuilder()

    cell = builder.build(
        cluster,
        event,
    )

    assert cell.beat == 4

    assert (
        cell.absolute_time_seconds
        == 1.012
    )

    assert (
        cell.offset_ms
        == pytest.approx(12.0)
    )

    assert (
        cell.metric_cluster_id
        == cluster_id
    )
