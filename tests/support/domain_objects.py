from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from jga.domain.beat_reference import BeatReference
from jga.domain.behaviour_observation import BehaviourObservation
from jga.domain.elementary_metric_event import ElementaryMetricEvent
from jga.domain.internal_metric_timeline import InternalMetricTimeline
from jga.domain.metric_cluster import MetricCluster
from jga.domain.pulse import Pulse


_NOW = datetime(2026, 1, 1)


def make_elementary_metric_event() -> ElementaryMetricEvent:
    return ElementaryMetricEvent(
        id=uuid4(),
        contributor_id=uuid4(),
        timestamp=0.0,
        confidence=1.0,
        created_at=_NOW,
    )


def make_beat_reference() -> BeatReference:
    return BeatReference(
        id=uuid4(),
        index=0,
        timestamp=0.0,
        created_at=_NOW,
    )


def make_metric_cluster() -> MetricCluster:
    return MetricCluster(
        id=uuid4(),
        beat_reference=make_beat_reference(),
        events=(make_elementary_metric_event(),),
        created_at=_NOW,
    )


def make_pulse() -> Pulse:
    return Pulse(
        id=uuid4(),
        index=0,
        cluster=make_metric_cluster(),
        timestamp=0.0,
        created_at=_NOW,
    )


def make_internal_metric_timeline() -> InternalMetricTimeline:
    pulse = make_pulse()

    return InternalMetricTimeline(
        id=uuid4(),
        pulses=(pulse,),
        created_at=_NOW,
    )


def make_behaviour_observation() -> BehaviourObservation:
    timeline = make_internal_metric_timeline()

    return BehaviourObservation(
        id=uuid4(),
        timeline=timeline,
        first_pulse=timeline.first_pulse,
        last_pulse=timeline.last_pulse,
        created_at=_NOW,
    )
