
from datetime import datetime
from uuid import uuid4

from jga.domain.beat_reference import BeatReference

from jga.domain.elementary_metric_event import (
    ElementaryMetricEvent,
)

from jga.domain.metric_cluster import (
    MetricCluster,
)

from jga.domain.pulse import Pulse

from jga.domain.internal_metric_timeline import (
    InternalMetricTimeline,
)

from jga.domain.services.behaviour_construction_builder import (
    BehaviourConstructionBuilder,
)


def test_behaviour_construction_builder_creates_profile_from_timeline():

    now = datetime.now()

    event = ElementaryMetricEvent(
        id=uuid4(),
        contributor_id=uuid4(),
        timestamp=0.0,
        confidence=1.0,
        created_at=now,
    )

    beat = BeatReference(
        id=uuid4(),
        index=0,
        timestamp=0.0,
        created_at=now,
    )

    cluster = MetricCluster(
        id=uuid4(),
        beat_reference=beat,
        events=(event,),
        created_at=now,
    )

    pulse = Pulse(
        id=uuid4(),
        index=0,
        cluster=cluster,
        timestamp=0.0,
        created_at=now,
    )

    timeline = InternalMetricTimeline(
        id=uuid4(),
        pulses=(pulse,),
        created_at=now,
    )

    builder = BehaviourConstructionBuilder()

    result = builder.build(
        timeline,
    )

    assert result.behaviour_profile is not None
    assert len(result.behaviour_observations) == 1
