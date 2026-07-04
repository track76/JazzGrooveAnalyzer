import pytest

from jga.core.domain.services.metric_contributor_resolver import (
    MetricContributorResolver,
)


def test_resolver_can_be_instantiated():
    resolver = MetricContributorResolver()

    assert resolver is not None


def test_resolve_requires_argument():
    resolver = MetricContributorResolver()

    with pytest.raises(TypeError):
        resolver.resolve()