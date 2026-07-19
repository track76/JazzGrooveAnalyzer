from datetime import datetime
from uuid import uuid4

import pytest

from jga.domain.metric_contributor import MetricContributor
from jga.domain.services.metric_contributor_resolver import (
    MetricContributorResolver,
)


def create_contributor():

    source_id = uuid4()

    contributor = MetricContributor(
        id=uuid4(),
        sound_source_id=source_id,
        musical_function_id=uuid4(),
        active=True,
        created_at=datetime.now(),
    )

    return source_id, contributor


def test_resolver_can_be_instantiated():

    resolver = MetricContributorResolver()

    assert resolver is not None


def test_resolve_requires_argument():

    resolver = MetricContributorResolver()

    with pytest.raises(TypeError):
        resolver.resolve()


def test_resolve_returns_matching_metric_contributor():

    resolver = MetricContributorResolver()

    source_id, contributor = create_contributor()

    result = resolver.resolve(
        source_id,
        (contributor,),
    )

    assert result is contributor
    assert result.sound_source_id == source_id


def test_resolve_raises_when_source_is_unknown():

    resolver = MetricContributorResolver()

    _, contributor = create_contributor()

    with pytest.raises(ValueError):
        resolver.resolve(
            uuid4(),
            (contributor,),
        )
