from datetime import datetime
from uuid import uuid4

from jga.core.stability_curve import StabilityCurve

from jga.domain.behaviour_descriptor import BehaviourDescriptor
from jga.domain.behaviour_observation import BehaviourObservation
from jga.domain.behaviour_quantification_context import (
    BehaviourQuantificationContext,
)
from jga.domain.internal_metric_timeline import (
    InternalMetricTimeline,
)
from jga.domain.pulse import Pulse

from jga.domain.services.behaviour_quantification_builder import (
    BehaviourQuantificationBuilder,
)

from jga.domain.services.behaviour_profile_builder import (
    BehaviourProfileBuilder,
)

from tests.support.domain_objects import (
    make_behaviour_observation,
    make_metric_cluster,
)


def test_quantification_builder_returns_descriptors():

    profile = BehaviourProfileBuilder().build(
        (
            make_behaviour_observation(),
        )
    )

    context = BehaviourQuantificationContext(
        behaviour_profile=profile,
        stability_curve=StabilityCurve(),
    )

    descriptors = (
        BehaviourQuantificationBuilder().build(context)
    )

    assert len(descriptors) == 1

    assert isinstance(
        descriptors[0],
        BehaviourDescriptor,
    )

    assert descriptors[0].name == "TemporalContinuity"

    assert descriptors[0].value == 1.0


def test_temporal_continuity_detects_fragmented_sequence():

    pulses = (
        Pulse(
            id=uuid4(),
            index=0,
            cluster=make_metric_cluster(),
            timestamp=0.0,
            created_at=datetime.now(),
        ),
        Pulse(
            id=uuid4(),
            index=1,
            cluster=make_metric_cluster(),
            timestamp=1.0,
            created_at=datetime.now(),
        ),
        Pulse(
            id=uuid4(),
            index=5,
            cluster=make_metric_cluster(),
            timestamp=2.0,
            created_at=datetime.now(),
        ),
        Pulse(
            id=uuid4(),
            index=6,
            cluster=make_metric_cluster(),
            timestamp=3.0,
            created_at=datetime.now(),
        ),
    )

    observation = BehaviourObservation(
        id=uuid4(),
        timeline=InternalMetricTimeline(
            id=uuid4(),
            pulses=pulses,
            created_at=datetime.now(),
        ),
        first_pulse=pulses[0],
        last_pulse=pulses[-1],
        created_at=datetime.now(),
    )

    profile = BehaviourProfileBuilder().build(
        (observation,),
    )

    context = BehaviourQuantificationContext(
        behaviour_profile=profile,
        stability_curve=StabilityCurve(),
    )

    descriptors = (
        BehaviourQuantificationBuilder().build(context)
    )

    assert descriptors[0].name == "TemporalContinuity"

    assert descriptors[0].value == 0.5
