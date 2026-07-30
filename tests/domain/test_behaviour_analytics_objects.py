from datetime import datetime
from uuid import uuid4

from jga.domain.analytical_structure import AnalyticalStructure
from jga.domain.behaviour_analytics import BehaviourAnalytics
from jga.domain.behaviour_observation import BehaviourObservation
from jga.domain.behaviour_observation_collection import (
    BehaviourObservationCollection,
)
from jga.domain.behaviour_profile import BehaviourProfile
from jga.domain.descriptor_set import DescriptorSet


def test_behaviour_domain_objects():

    observation = BehaviourObservation(
        id=uuid4(),
        timeline=None,
        first_pulse=None,
        last_pulse=None,
        created_at=None,
    )

    collection = BehaviourObservationCollection(
        observations=(observation,),
    )

    descriptor_set = DescriptorSet(
        descriptors=(),
    )

    profile = BehaviourProfile(
        id=uuid4(),
        observations=(observation,),
        created_at=datetime.now(),
    )

    analytics = BehaviourAnalytics(
        profile=profile,
    )

    structure = AnalyticalStructure(
        source_descriptor_set=descriptor_set,
    )

    assert collection.observations == (observation,)
    assert profile.observations == (observation,)
    assert profile.observation_count == 1
    assert analytics.profile is profile
    assert structure.source_descriptor_set is descriptor_set
