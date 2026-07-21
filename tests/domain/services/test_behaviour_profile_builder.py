from datetime import datetime
from uuid import uuid4

from jga.domain.behaviour_observation import BehaviourObservation
from jga.domain.behaviour_profile import BehaviourProfile
from jga.domain.beat_reference import BeatReference
from jga.domain.elementary_metric_event import ElementaryMetricEvent
from jga.domain.internal_metric_timeline import InternalMetricTimeline
from jga.domain.metric_cluster import MetricCluster
from jga.domain.pulse import Pulse
from jga.domain.services.behaviour_profile_builder import BehaviourProfileBuilder


def make_pulse(index: int) -> Pulse:
    event = ElementaryMetricEvent(
        id=uuid4(),
        contributor_id=uuid4(),
        timestamp=float(index),
        confidence=1.0,
        created_at=datetime.now(),
    )

    beat = BeatReference(
        id=uuid4(),
        index=index,
        timestamp=float(index),
        created_at=datetime.now(),
    )

    cluster = MetricCluster(
        id=uuid4(),
        beat_reference=beat,
        events=(event,),
        created_at=datetime.now(),
    )

    return Pulse(
        id=uuid4(),
        index=index,
        cluster=cluster,
        timestamp=float(index),
        created_at=datetime.now(),
    )


def make_observation() -> BehaviourObservation:
    pulse = make_pulse(0)

    timeline = InternalMetricTimeline(
        id=uuid4(),
        pulses=(pulse,),
        created_at=datetime.now(),
    )

    return BehaviourObservation(
        id=uuid4(),
        timeline=timeline,
        first_pulse=pulse,
        last_pulse=pulse,
        created_at=datetime.now(),
    )


def test_build_profile():
    observation = make_observation()

    profile = BehaviourProfileBuilder().build((observation,))

    assert isinstance(profile, BehaviourProfile)
    assert profile.observation_count == 1
