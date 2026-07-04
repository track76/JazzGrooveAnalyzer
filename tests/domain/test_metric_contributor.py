from datetime import datetime
from uuid import uuid4

import pytest

from jga.core.domain.metric_contributor import MetricContributor


def test_create_valid_metric_contributor():
    contributor = MetricContributor(
        id=uuid4(),
        sound_source_id=uuid4(),
        musical_function_id=uuid4(),
        active=True,
        created_at=datetime.now(),
    )

    assert contributor.active is True


def test_inactive_metric_contributor():
    contributor = MetricContributor(
        id=uuid4(),
        sound_source_id=uuid4(),
        musical_function_id=uuid4(),
        active=False,
        created_at=datetime.now(),
    )

    assert contributor.active is False


def test_invalid_active_type_raises():
    with pytest.raises(TypeError):
        MetricContributor(
            id=uuid4(),
            sound_source_id=uuid4(),
            musical_function_id=uuid4(),
            active="yes",
            created_at=datetime.now(),
        )